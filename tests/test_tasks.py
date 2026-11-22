import unittest
from tasks import agregar_tarea, completar_tarea, pendientes

class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "Estudio")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])
        self.assertEqual(tarea["categoria"], "Estudio")

    def test_categoria_vacia(self):
        tareas = []
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer", "")
        with self.assertRaises(ValueError):
            agregar_tarea(tareas, "Leer", "   ")
        self.assertEqual(tareas, [])

    def test_filtrar_pendientes_por_categoria(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        agregar_tarea(tareas, "B", "Casa")
        agregar_tarea(tareas, "C", "estudio")
        completar_tarea(tareas, 3)
        self.assertEqual([t["titulo"] for t in pendientes(tareas, "ESTUDIO")], ["A"])
        self.assertEqual(len(pendientes(tareas)), 2)

    def test_filtrar_categoria_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        self.assertEqual(pendientes(tareas, "Otra"), [])

    def test_filtrar_categoria_vacia_o_espacios(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        agregar_tarea(tareas, "B", "Casa")
        self.assertEqual(pendientes(tareas, ""), [])
        self.assertEqual(pendientes(tareas, "   "), [])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar", "Estudio")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

if __name__ == "__main__":
    unittest.main()
