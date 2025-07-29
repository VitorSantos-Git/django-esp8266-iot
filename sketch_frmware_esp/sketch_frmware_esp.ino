#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include "password_ssid.h"

//Pinagem do ESP8266 Pinos Digitais (GPIO):
#define D0 16
#define D1 5
#define D2 4
#define D3 0
#define D4 2
#define D5 14
#define D6 12
#define D7 13
#define D8 15

// --- Configurações de Rede ---
const char* ssid = txtssid;
const char* password = txtpassword;

// --- Configurações do Servidor Django (AGORA COM SEU IP E A URL DA API) ---
// MUDAR 'SEU_IP_DO_SERVIDOR_DJANGO' PARA O IP REAL DO SEU COMPUTADOR (ex: 192.168.1.100)
const char* djangoServerBaseUrl = "http://192.168.31.80:8000/api/device/";
const char* DEVICE_ID = "ESP8266_002"; // O ID ÚNICO DESTE DISPOSITIVO

// Substitua "SEU_TOKEN_GERADO_AQUI" pelo token real do seu usuário/dispositivo!
const char* AUTH_TOKEN = txtToken;

// --- Variáveis para controle do dispositivo (exemplo) ---
int temperature = 0;
int humidity = 0;
bool relayState = false;

// --- Função para conectar ao Wi-Fi ---
void connectWiFi() {
  Serial.print("Conectando-se a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

// --- Função auxiliar para adicionar o cabeçalho de autenticação ---
void addAuthHeader(HTTPClient& http) {
  String authHeader = "Token ";
  authHeader += AUTH_TOKEN;
  http.addHeader("Authorization", authHeader);
}

// --- Função para enviar dados ao Django ---
void sendDataToDjango() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String postUrl = String(djangoServerBaseUrl);
    http.begin(client, postUrl);
    http.addHeader("Content-Type", "application/json");
    addAuthHeader(http);

    // Cria um objeto JSON para enviar os dados
    // Aumentei o tamanho do buffer JSON para 500 para dados genéricos futuros
    StaticJsonDocument<500> doc;
    // O device_id deve ser ÚNICO para cada ESP. Mude se for gravar em outro ESP!
    doc["device_id"] = DEVICE_ID;
    doc["name"] = WiFi.localIP().toString(); // IP
    doc["device_type"] = "Sala de Aula"; // Tipo do dispositivo
    doc["location"] = "SalaXXXX"; // Localização do dispositivo

    // Dados específicos do sensor dentro de um objeto 'data'
    JsonObject data_obj = doc.createNestedObject("data");
    data_obj["temperature_celsius"] = temperature;
    data_obj["humidity_percent"] = humidity;
    data_obj["relay_state_D1"] = relayState;
    // Adicione outros dados aqui conforme seus sensores, ex:
    // data_obj["luminosity_lux"] = 140;

    String jsonString;
    serializeJson(doc, jsonString);

    Serial.print("Enviando dados: ");
    Serial.println(jsonString);

    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code (POST): ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error code (POST): ");
      Serial.println(httpResponseCode);
      Serial.print("HTTP Error (POST): ");
      Serial.println(http.errorToString(httpResponseCode));
    }
    http.end();
  } else {
    Serial.println("Wi-Fi não conectado, não foi possível enviar dados.");
  }
}

// --- Função para enviar Confirmação de Comando Executado ---
void sendCommandExecutedConfirmation(const char* executedCommand, const char* target) {
    if (WiFi.status() == WL_CONNECTED) {
        WiFiClient client;
        HTTPClient http;

        String putUrl = String(djangoServerBaseUrl) + String(DEVICE_ID) + "/";
        http.begin(client, putUrl);
        http.addHeader("Content-Type", "application/json");
        addAuthHeader(http);

        StaticJsonDocument<200> doc; // Buffer menor, pois só enviamos 2 campos
        doc["last_command"] = executedCommand;
        doc["pending_command"] = nullptr; // ZERA O CAMPO PENDING_COMMAND APÓS A EXECUÇÃO
        
        // Formata a data/hora atual no formato ISO 8601 esperado pelo Django
        // Ex: "2025-07-22T17:30:00.000Z"
        // Nota: ESP8266 não tem RTC nativo, então esta hora será baseada no uptime ou NTP se configurado.
        // Para simplicidade, vamos usar um placeholder ou você pode integrar um módulo NTP.
        // Por enquanto, o Django registrará o tempo da requisição PUT.
        // Se você quiser que o ESP envie a hora exata da execução:
        // String timestamp;
        // if (timeClient.update()) { // Se estiver usando NTP
        //    timestamp = timeClient.getFormattedTime(); // Adapte para seu formato
        // } else {
        //    timestamp = "YYYY-MM-DDTHH:MM:SSZ"; // Placeholder
        // }
        // doc["last_command_at"] = timestamp;

        // Na verdade, o campo `last_command_at` será atualizado com `timezone.now()` no lado do Django
        // quando a requisição PUT chegar. Então não precisamos enviá-lo do ESP,
        // a menos que você queira uma precisão de tempo muito maior baseada no relógio do ESP/NTP.
        // Para simplicidade, vamos deixar o Django cuidar do timestamp.

        String jsonString;
        serializeJson(doc, jsonString);

        Serial.print("Enviando confirmação de comando (PUT): ");
        Serial.println(jsonString);

        int httpResponseCode = http.PUT(jsonString); // Use PUT!

        if (httpResponseCode > 0) {
            Serial.print("HTTP Response code (PUT): ");
            Serial.println(httpResponseCode);
            String response = http.getString();
            Serial.println(response);
        } else {
            Serial.print("Error code (PUT): ");
            Serial.println(httpResponseCode);
            Serial.print("HTTP Error (PUT): ");
            Serial.println(http.errorToString(httpResponseCode));
        }
        http.end();
    } else {
        Serial.println("Wi-Fi não conectado, não foi possível enviar confirmação.");
    }
}

// --- Função para receber comandos do Django (vamos desenvolver isso mais tarde) ---
void receiveCommandsFromDjango() {
  if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;

      // Constrói a URL para GET (adiciona o device_id ao final)
      String getUrl = String(djangoServerBaseUrl) + String(DEVICE_ID) + "/";
      http.begin(client, getUrl);
      addAuthHeader(http);
      
      Serial.print("Verificando por comandos em: ");
      Serial.println(getUrl);

      int httpResponseCode = http.GET();

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code (GET): ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.print("Resposta do servidor (GET): ");
        Serial.println(payload);

        // Processa a resposta JSON
        StaticJsonDocument<500> doc; // Aumentar se a resposta for muito grande
        DeserializationError error = deserializeJson(doc, payload);

        if (error) {
          Serial.print(F("deserializeJson() falhou com o código: "));
          Serial.println(error.f_str());
          return;
        }

        const char* status = doc["status"]; // Obtém o status da resposta

        if (strcmp(status, "command_pending") == 0) { 
          // Comando pendente encontrado!
          Serial.println("COMANDO PENDENTE RECEBIDO!");
          if (doc.containsKey("command") && !doc["command"].isNull()) {  
            JsonObject command =  doc["command"]; // Pega o objeto pending_command do JSON

            const char* action = command["action"];
            const char* target = command["target"];
            int value = command["value"] | 0; // Valor padrão 0 se não existir

            Serial.print("Ação: "); Serial.println(action);
            Serial.print("Alvo: "); Serial.println(target);
            Serial.print("Valor: "); Serial.println(value);

            // --- LÓGICA PARA EXECUTAR O COMANDO E ATUALIZAR O ESTADO INTERNO ---
            // Aqui iremos adicionar os código para controlar o hardware
            if (strcmp(action, "ligar_rele") == 0 && strcmp(target, "rele_D1") == 0) {
                relayState = true;
                Serial.println("Rele D1 LIGADO!");
                sendCommandExecutedConfirmation("ligar_rele", "rele_D1"); // Confirmar execução
            } else if (strcmp(action, "desligar_rele") == 0 && strcmp(target, "rele_D1") == 0) {
                relayState = false;
                Serial.println("Rele D1 DESLIGADO!");
                sendCommandExecutedConfirmation("desligar_rele", "rele_D1");
            } 
            // Adicione mais blocos 'else if' para outros comandos:
            //exemplo
            // else if (strcmp(action, "tocar_musica") == 0) {
            //     // Lógica para tocar música
            // }
            // else if (strcmp(action, "emitir_ir") == 0) {
            //     // Lógica para emitir sinal IR
            // }
            // ... etc.

            // --- ATUALIZAR Os PINOs IMEDIATAMENTE APÓS RECEBER O COMANDO ---
            update_saida(); // Garante que a saída é atualizada na hora!
          }else {
             Serial.println("Status 'command_pending' mas objeto 'command' não encontrado ou nulo.");
          }
        } else if (strcmp(status, "no_command") == 0) {
          Serial.println("Nenhum comando pendente.");
         } else {
           Serial.print("Status de resposta desconhecido: ");
           Serial.println(status);
        }
      } else {
        Serial.print("Error code (GET): ");
        Serial.println(httpResponseCode);
        Serial.print("HTTP Error (GET): ");
        Serial.println(http.errorToString(httpResponseCode));
      }
      http.end();
    } else {
      Serial.println("Wi-Fi não conectado, não foi possível verificar comandos.");
    }
}

void conf_GPIO_init(){
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  pinMode(D1, OUTPUT); // Configura o pino D1 (GPIO5) como saída para o relé
  digitalWrite(D1, LOW); // Garante que o relé comece desligado
}

void pisca_led(){
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); 
}

void update_saida(){
  digitalWrite(D1, relayState ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);
  delay(100);
  connectWiFi();

  conf_GPIO_init();
}

void loop() {
  temperature = random(20, 35);
  humidity = random(40, 70);
  pisca_led();
  update_saida();

  sendDataToDjango();
  delay(1000);
  receiveCommandsFromDjango();

  delay(4000); // Envia dados a cada 5 segundos
}