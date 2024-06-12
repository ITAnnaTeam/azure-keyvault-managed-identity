import os

from flask import (
    Flask,
    render_template,
    send_from_directory,
)
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)


@app.route("/")
def index():
    print("Request for index page received")
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/managedidentity", methods=["POST"])
def managedidentity():
    key_vault_url = "https://itannapythonflask.vault.azure.net/"
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    secret_name = "databasepasswordkey"
    retrieved_secret = secret_client.get_secret(secret_name)
    return render_template("managedidentity.html", secret=retrieved_secret.value)


@app.route("/usermanagedidentity", methods=["POST"])
def usermanagedidentity():
    key_vault_url = "https://itannapythonflask.vault.azure.net/"
    credential = DefaultAzureCredential(managed_identity_client_id="5484074f-bdca-4126-b3e6-cd614089aacb", additionally_allowed_tenants=['*'])
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    secret_name = "databasepasswordkey"
    retrieved_secret = secret_client.get_secret(secret_name)
    return render_template("usermanagedidentity.html", secret=retrieved_secret.value)

if __name__ == "__main__":
    app.run()
