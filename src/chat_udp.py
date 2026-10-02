import argparse
import socket
import threading


def puerto(valor):
    numero = int(valor)
    if not 1 <= numero <= 65535:
        raise argparse.ArgumentTypeError("el puerto debe estar entre 1 y 65535")
    return numero


def recibir(sock, detener):
    while not detener.is_set():
        try:
            datos, origen = sock.recvfrom(65535)
            print(f"\n{origen[0]}:{origen[1]} > {datos.decode('utf-8', errors='replace')}")
        except socket.timeout:
            continue
        except OSError as error:
            if not detener.is_set():
                print(f"\nError al recibir: {error}")
            break


def main():
    parser = argparse.ArgumentParser(description="Chat directo entre dos equipos mediante UDP")
    parser.add_argument("puerto_local", type=puerto)
    parser.add_argument("ip_remota")
    parser.add_argument("puerto_remoto", type=puerto)
    args = parser.parse_args()

    detener = threading.Event()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0", args.puerto_local))
            sock.settimeout(0.5)
            hilo = threading.Thread(target=recibir, args=(sock, detener), daemon=True)
            hilo.start()
            print("Escribe mensajes y presiona Enter. Usa /salir para terminar.")

            try:
                while True:
                    mensaje = input("Tú > ")
                    if mensaje == "/salir":
                        break
                    sock.sendto(mensaje.encode("utf-8"), (args.ip_remota, args.puerto_remoto))
            finally:
                detener.set()
                hilo.join()
    except OSError as error:
        raise SystemExit(f"Error de red: {error}") from error
    except (KeyboardInterrupt, EOFError):
        pass


if __name__ == "__main__":
    main()
