from apps.Util_apps.LogProject import logging
import apps.Util_apps.Util as Util


def funcion_si_respuesta_es_correcta(response_json):
    logging.info(response_json)


def funcion_si_respuesta_no_es_correcta(url):
    logging.error("No se ha podido realizar la peticion a la url {}".format(url))


if __name__ == "__main__":
    Util.generate_request_get(url="https://randomuser.me/api",
                              success_callback=funcion_si_respuesta_es_correcta,
                              error_callback=funcion_si_respuesta_no_es_correcta)