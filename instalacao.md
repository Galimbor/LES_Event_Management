
### Instalação

1. Abrir o terminal na pasta do seu computador onde vai ser guardado o projeto e colar a pasta com código enviado

e.g.:
```SH
cd ~/LES/
```


3. Entrar na pasta do projeto

```SH
cd LES_G1/src
```

4. Criar o ambiente do projeto (venv)

**Atenção: A versão de Python com a qual criar o ambiente do projeto deve ser igual para todos**


Se a versão do Python estiver correta, segue a criação do ambiente (na pasta do projeto):

Linux:
```SH
python3 -m venv env
```

Windows:
```SH
python -m venv env
```

5. Ativar o ambiente virtual no terminal

Linux:
```SH
source env/bin/activate
```

Windows:
```SH
env\Scripts\activate
```

Em Windows às vezes há problemas neste passo. Se der ErrorSecurityPolicy, ou algo do género, tentar isto na mesma shell:
```SH
Set-ExecutionPolicy Unrestricted -Force
env\Scripts\activate
```

A extensão padrão de Python do VSCode tem a opção de ativar automaticamente o ambiente em novos terminais. Para ativar a funcionalidade, há que abrir a **Palete de Comandos (F1)**,  **Python: Selecionar Interpretador** e escolher a opção cuja localização comece com `./env` ou `.\env`.

6. Atualizar as dependências iniciais do ambiente

```SH
pip install --upgrade pip setuptools
```

7. Instalar MySQL
```SH
brew install mysql
```

8.  Instalar as dependências do projeto

```SH
pip install -r requirements.txt
```


#### Iniciar o servidor localmente

```SH
python manage.py runserver
```


#### Desativar o ambiente virtual no terminal

```SH
deactivate
```

#### Instalar nova dependência

```SH
pip install nome_da_dependência && pip freeze > requirements.txt
```

#### Instalar lista de dependências necessárias

```SH
pip install -r requirements.txt
```





