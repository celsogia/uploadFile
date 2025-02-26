import functions_framework
from flask import request, jsonify
from google.cloud import storage

# Configuração do bucket de armazenamento
BUCKET_NAME = "bucket-ocr-pedidos-faturamento"

# Inicializa o cliente do Cloud Storage
storage_client = storage.Client()

@functions_framework.http
def upload_arquivo(request):
    """Recebe um arquivo via API e armazena no Cloud Storage."""
    
    if request.method != "POST":
        return jsonify({"error": "Método não permitido. Use POST"}), 405

    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    
    # Verifica se é uma extensão válida
    extensoes_permitidas = {"jpg", "jpeg", "png", "pdf"}
    if not file.filename or file.filename.split(".")[-1].lower() not in extensoes_permitidas:
        return jsonify({"error": "Formato inválido. Apenas JPEG, PNG e PDF são permitidos"}), 400

    # Salva no Cloud Storage
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

    return jsonify({
        "message": "Upload realizado com sucesso!",
        "file_url": f"gs://{BUCKET_NAME}/{file.filename}"
    })
