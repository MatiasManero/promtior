"""
Consola interactiva para chatear con el bot de Promtior.
"""

from rag import chain


def run_console() -> None:
    """
    Bucle principal: lee la pregunta del usuario, invoca la cadena y muestra la respuesta.
    Salir con 'salir', 'exit' o Ctrl+C.
    """
    print("\n  Chatbot de Promtior - Consola interactiva")
    print("  " + "=" * 50)
    print("  Escribe tu pregunta y pulsa Enter.")
    print("  Para salir: escribe 'salir' o 'exit', o pulsa Ctrl+C.\n")

    while True:
        try:
            question = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break

        if not question:
            continue

        if question.lower() in ("salir", "exit", "quit", "q"):
            print("Hasta luego.")
            break

        try:
            answer = chain().invoke(question)
            print(f"\nBot: {answer}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    run_console()
