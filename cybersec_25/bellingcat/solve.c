#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/evp.h>
#include <openssl/md5.h>
#include <openssl/bio.h>
#include <openssl/buffer.h>
#include <omp.h> // Per il multithreading

// --- CONFIGURAZIONE ---
const char *CIPHERTEXT_B64 = "U2FsdGVkX18bFYOs0Qxt4NjMQ5g+lxOzbOuCRB2RG3Q2fw4mKC93xKIpFnH8Mo6h";
const char *TARGET_STRING = "Answer Correct";

// Parametri CryptoJS
#define KEY_LEN 32
#define IV_LEN 16
#define SALT_LEN 8
#define HEADER_LEN 8 // "Salted__"

// Funzione helper per decodificare Base64 usando OpenSSL
int base64_decode(const char *b64message, unsigned char **buffer, size_t *length) {
    BIO *bio, *b64;
    int decodeLen = strlen(b64message);
    *buffer = (unsigned char *)malloc(decodeLen);
    bio = BIO_new_mem_buf(b64message, -1);
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
    *length = BIO_read(bio, *buffer, decodeLen);
    BIO_free_all(bio);
    return 0;
}

// Implementazione manuale ottimizzata di EVP_BytesToKey (MD5)
// CryptoJS usa: MD5(Pass + Salt) -> D1, MD5(D1 + Pass + Salt) -> D2, ecc...
void derive_key_iv_optimized(const char *password, const unsigned char *salt, unsigned char *key, unsigned char *iv) {
    unsigned char d[16]; // MD5 digest size
    unsigned char d_tot[48]; // Key (32) + IV (16) = 48 bytes
    MD5_CTX c;
    int pass_len = strlen(password);
    int bytes_filled = 0;

    // Round 1
    MD5_Init(&c);
    MD5_Update(&c, password, pass_len);
    MD5_Update(&c, salt, SALT_LEN);
    MD5_Final(d, &c);
    memcpy(d_tot, d, 16);
    bytes_filled += 16;

    // Round 2
    MD5_Init(&c);
    MD5_Update(&c, d, 16);
    MD5_Update(&c, password, pass_len);
    MD5_Update(&c, salt, SALT_LEN);
    MD5_Final(d, &c);
    memcpy(d_tot + 16, d, 16);
    bytes_filled += 16;

    // Round 3 (Serve solo per finire l'IV)
    MD5_Init(&c);
    MD5_Update(&c, d, 16);
    MD5_Update(&c, password, pass_len);
    MD5_Update(&c, salt, SALT_LEN);
    MD5_Final(d, &c);
    memcpy(d_tot + 32, d, 16);

    // Copia nei buffer finali
    memcpy(key, d_tot, KEY_LEN);
    memcpy(iv, d_tot + KEY_LEN, IV_LEN);
}

int main() {
    // 1. Decodifica il Base64
    unsigned char *data;
    size_t data_len;
    base64_decode(CIPHERTEXT_B64, &data, &data_len);

    // 2. Verifica Header e Estrai Salt
    if (strncmp((const char*)data, "Salted__", HEADER_LEN) != 0) {
        printf("Errore: Formato OpenSSL non valido (manca l'header Salted__)\n");
        return 1;
    }

    unsigned char salt[SALT_LEN];
    memcpy(salt, data + HEADER_LEN, SALT_LEN);

    // Il vero ciphertext inizia dopo Header + Salt
    unsigned char *ciphertext = data + HEADER_LEN + SALT_LEN;
    int ciphertext_len = data_len - HEADER_LEN - SALT_LEN;

    printf("🚀 Avvio Brute-Force in C (OpenMP) su 10.000.000 chiavi...\n");
    printf("Target: '%s'\n", TARGET_STRING);

    int found = 0;

    // 3. Loop Parallelo con OpenMP
    #pragma omp parallel for schedule(dynamic) shared(found)
    for (int i = 0; i < 10000000; i++) {
        // Se già trovato da un altro thread, salta (flush non garantito istantaneamente ma ok per brute force)
        if (found) continue;

        // Genera la chiave stringa "0000123"
        char pass[8];
        sprintf(pass, "%07d", i);

        // Deriva Key e IV
        unsigned char key[KEY_LEN];
        unsigned char iv[IV_LEN];
        derive_key_iv_optimized(pass, salt, key, iv);

        // Prepara il contesto di decifratura
        EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
        unsigned char decrypted[1024]; // Buffer sicuro
        int len;
        int plaintext_len;

        // Tenta la decifratura AES-256-CBC
        if (EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv) != 1) {
            EVP_CIPHER_CTX_free(ctx);
            continue;
        }

        // Disabilita padding automatico per evitare errori "bad decrypt" rumorosi,
        // gestiamo noi la ricerca della stringa nel blocco grezzo.
        // Oppure, lasciamolo attivo e controlliamo il return di Final.
        // Per velocità e robustezza, controlliamo Final.

        int update_ok = EVP_DecryptUpdate(ctx, decrypted, &len, ciphertext, ciphertext_len);
        plaintext_len = len;

        int final_ok = EVP_DecryptFinal_ex(ctx, decrypted + len, &len);
        plaintext_len += len;

        EVP_CIPHER_CTX_free(ctx);

        if (final_ok == 1) {
            // Aggiungi terminatore null per sicurezza stringa
            decrypted[plaintext_len] = '\0';

            // Cerca la stringa target
            if (strstr((char *)decrypted, TARGET_STRING)) {
                #pragma omp critical
                {
                    printf("\n========================================\n");
                    printf("🔓 SUCCESSO! Trovato dal thread %d\n", omp_get_thread_num());
                    printf("🔑 CHIAVE: %s\n", pass);
                    printf("📄 MESSAGGIO: %s\n", decrypted);
                    printf("========================================\n");
                    found = 1;
                }
            }
        }

        // Feedback progress ogni 500k (solo thread 0)
        if (i % 500000 == 0 && omp_get_thread_num() == 0) {
            printf("\rChecking... %s", pass);
            fflush(stdout);
        }
    }

    free(data);
    if (!found) printf("\n❌ Nessuna chiave trovata.\n");
    return 0;
}