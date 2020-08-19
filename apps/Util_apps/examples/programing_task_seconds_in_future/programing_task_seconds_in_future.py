from apps.Util_apps.Decoradores import execute_in_thread_timer


@execute_in_thread_timer(seconds=2)
def callback():
    print("probando")


if __name__ == "__main__":
    callback()
    print("Iniciando...")
