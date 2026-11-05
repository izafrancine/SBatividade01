# Item 4

1. Abra o primeiro terminal e inicie o servidor

`python ServidorMonitor.py`


2. Abra o segundo terminal e entre como primeiro Worker 

`python Worker.py Worker_1`


3. Abra o terceiro terminal e entre como segundo Worker 

`python Worker.py Worker_2` 

4. Inicie 

A cada 3 segundos envia a mensagem PING Worker_1 (o ID vem do argumento do comando). Pode abrir quantos workers quiser, cada um com um ID diferente.

5. Encerre

Nos Worker's, aperte Crtl+C para simular uma falha. Para encerrar, aperte Crtl+C no terminal do servidor. 

