# Cofre de Credenciais

Aplicação web para armazenamento seguro de senhas e credenciais.

## Descrição

O Cofre de Credenciais é uma aplicação web que permite aos usuários armazenar suas credenciais de maneira segura. Funcionalidades incluem autenticação de usuários, CRUD de credenciais isolado por usuário (um usuário não vê a senha do outro), criptografia das senhas no banco usando Fernet, e um gerador de senhas fortes integrado no frontend.

## Funcionalidades

- **Autenticação**: Gerenciamento de usuários com Flask-Login.
- **CRUD de Credenciais**: Adicionar, remover, atualizar e listar credenciais para cada usuário.
- **Criptografia**: Armazenamento seguro de senhas usando a biblioteca Cryptography.
- **Gerador de Senhas Fortes**: Integração com HTML/JS puro.

## Stack

- Python
- Flask
- SQLite
- Flask-Login
- Cryptography
- HTML/JS puro
- Bootstrap 5

## Como rodar localmente

1. **Criar o ambiente virtual**:
   ```sh
   python3 -m venv venv
   ```

2. **Ativar o ambiente**:
   ```sh
   source venv/bin/activate
   ```

3. **Instalar dependências**:
   ```sh
   pip install flask flask-sqlalchemy flask-login cryptography
   ```

4. **Executar**:
   ```sh
   python3 app.py
   ```

## Segurança

O aplicativo exige uma chave de criptografia. O próprio código já gera uma aleatória caso não exista, mas em produção é necessário definir a variável de ambiente `ENCRYPTION_KEY`.