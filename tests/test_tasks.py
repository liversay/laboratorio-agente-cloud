import unittest
from tasks import agregar_tarea, completar_tarea, eliminar_tarea, pendientes

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

    def test_eliminar_tarea_existente(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        agregar_tarea(tareas, "B", "Casa")
        eliminada = eliminar_tarea(tareas, 1)
        self.assertEqual(eliminada["id"], 1)
        self.assertEqual(eliminada["titulo"], "A")
        self.assertEqual([t["id"] for t in tareas], [2])

    def test_eliminar_tarea_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        copia = [dict(t) for t in tareas]
        with self.assertRaises(ValueError) as ctx:
            eliminar_tarea(tareas, 99)
        self.assertEqual(str(ctx.exception), "Tarea no encontrada")
        self.assertEqual(tareas, copia)

    def test_eliminar_conserva_demas_tareas(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        agregar_tarea(tareas, "B", "Casa")
        agregar_tarea(tareas, "C", "Estudio")
        completar_tarea(tareas, 3)
        eliminar_tarea(tareas, 2)
        self.assertEqual(
            tareas,
            [
                {"id": 1, "titulo": "A", "categoria": "Estudio", "completada": False},
                {"id": 3, "titulo": "C", "categoria": "Estudio", "completada": True},
            ],
        )

    def test_eliminar_de_lista_vacia(self):
        tareas = []
        with self.assertRaises(ValueError) as ctx:
            eliminar_tarea(tareas, 1)
        self.assertEqual(str(ctx.exception), "Tarea no encontrada")
        self.assertEqual(tareas, [])

    def test_eliminar_dos_veces_el_mismo_id(self):
        tareas = []
        agregar_tarea(tareas, "A", "Estudio")
        agregar_tarea(tareas, "B", "Casa")
        primera = eliminar_tarea(tareas, 1)
        self.assertEqual(primera["id"], 1)
        copia = [dict(t) for t in tareas]
        with self.assertRaises(ValueError) as ctx:
            eliminar_tarea(tareas, 1)
        self.assertEqual(str(ctx.exception), "Tarea no encontrada")
        self.assertEqual(tareas, copia)

    def test_eliminar_del_medio_conserva_orden(self):
        tareas = []
        for titulo in ["A", "B", "C", "D"]:
            agregar_tarea(tareas, titulo, "Estudio")
        eliminar_tarea(tareas, 2)
        self.assertEqual([t["titulo"] for t in tareas], ["A", "C", "D"])
        self.assertEqual([t["id"] for t in tareas], [1, 3, 4])

if __name__ == "__main__":
    unittest.main()
