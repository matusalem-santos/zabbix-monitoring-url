# Objetivo 

Monitorar o health check das URL's

# Dependencias 

- python3 instalado
- biblioteca pyzabbix do python (Para instalar execute o comando: **pip3 install pyzabbix** certifique-se de que o python3 e o pip3 estão instalados na maquina)

# Execução do script 

- Colocar as URL's no arquivo **urls.txt** exemplo:
<img src="http://i.imgur.com/33YvHJf.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />

- Necessário o protocolo da url estar explícito (**http** ou **https**)
- Executar o script passando **"url" "usuario" "senha"** do zabbix como parametro, exemplo: 
```bash 
    ./create_monitoring_url.py "http://url-zabbix" "usuario" "senha" 
```
- Sera criado um host no Zabbix chamado **Monitoramento URL** que contera o monitoramento das URLs passadas no arquivo **urls.txt**