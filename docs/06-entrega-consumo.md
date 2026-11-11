# 06 · Entrega operativa y consumo (API / batch / streaming)

## 1. Modelo de entrega

| Modelo | Modo de entrega | Consumidor |
|---|---|---|
| Riesgo financiero | Batch (cartera) + API on-demand | App de crédito, BI, agente IA |
| Fraude | API real-time (streaming) | Motor transaccional, analistas |

## 2. API de consumo (gobernada)

- **Protocolo:** REST (JSON) con versionado en la URL (/v1/score).
- **Auth:** OAuth2 / mTLS; rate-limit por consumidor.
- **Contrato:** esquema de entrada/salida versionado (OpenAPI), compatible hacia atrás.
- **Endpoints:**

    POST /v1/risk/score        → { cliente_id, producto? } → { score, bucket, explicacion }
    POST /v1/fraud/score       → { transaccion }            → { score, decision, explicacion }
    GET  /v1/models            → { versiones activas, health }

- **Async:** eventos de scoring publicados a Kafka para consumidores de alto volumen.

## 3. Integración con el agente IA

El agente IA consume los modelos vía API para **explicar** y **accionar**:

- Consulta el score de riesgo y fraude de un cliente.
- Recibe la **explicación SHAP** y la traduce a lenguaje natural.
- Recomienda acciones (revisar alerta, ofrecer producto, ajustar cupo).
- El agente **no decide solo** en temas sensibles: escalamiento y aprobación humana donde aplique.

## 4. Acceso controlado

- API gateway con políticas por consumidor (scopes, cuotas, auditoría).
- Trazabilidad de cada scoring (quién consultó, qué resultado, con qué modelo).
- Entornos separados y secretos gestionados (vault/secrets manager).

## 5. Acuerdos de servicio

- Fraude: P95 < 100 ms, disponibilidad 99.9%.
- Riesgo batch: ventana nocturna definida; API on-demand P95 < 200 ms.
- Versionado de API compatible; deprecación con aviso previo.
