# Chat UDP P2P

Chat directo por terminal entre dos computadoras, hecho con Python 3 y su
biblioteca estándar. Cada instancia escucha en `0.0.0.0` y envía datagramas
UTF-8 al otro participante, sin servidor central.

## Uso en la misma red local

Busca la IP local de cada equipo:

- Windows: `ipconfig` (busca "Dirección IPv4").
- Linux: `ip addr`.
- macOS: `ipconfig getifaddr en0` (Wi-Fi).

Supongamos que el equipo A tiene `192.168.1.10` y el B `192.168.1.20`.

En el equipo A:

```powershell
python src/chat_udp.py 5000 192.168.1.20 5001
```

En el equipo B:

```powershell
python src/chat_udp.py 5001 192.168.1.10 5000
```

Escribe un mensaje y presiona Enter. Usa `/salir` para cerrar el programa y
liberar el socket. Si `python` no ejecuta Python 3, usa `python3`.

Ambos equipos deben permitir conexiones UDP entrantes al puerto local elegido.
En Windows se puede crear una regla de entrada en **Firewall de Windows con
seguridad avanzada**, seleccionando UDP y el puerto (5000 o 5001). En Linux
con UFW, por ejemplo: `sudo ufw allow 5000/udp`. Limita la regla a la red local
cuando sea posible.

## Prueba local

Abre dos terminales en este directorio. En la primera ejecuta:

```powershell
python src/chat_udp.py 5000 127.0.0.1 5001
```

En la segunda:

```powershell
python src/chat_udp.py 5001 127.0.0.1 5000
```

Envía mensajes desde ambas terminales y termina cada proceso con `/salir`.

## Limitaciones

UDP no garantiza entrega, orden ni ausencia de duplicados. Este ejemplo no
agrega retransmisiones ni confirmaciones. Para conectar equipos en redes
diferentes puede ser necesario configurar NAT/redirección de puertos o usar
una VPN.
