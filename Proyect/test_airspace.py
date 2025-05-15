import unittest
from airSpace import AirSpace
from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class TestAirSpace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        cls.airspace = AirSpace()
        
        # Crear datos de prueba
        cls.airspace.navpoints = [
            NavPoint(1, "GIR", 41.9313888889, 2.7716666667),
            NavPoint(2, "GODOX", 39.3725, 1.4108333333),
            NavPoint(3, "GRAUS", 41.979166667, 0.3763888889),
            NavPoint(4, "IZA", 38.8763888889, 1.385),
            NavPoint(5, "LEBL", 41.2971, 2.07846)  # Aeropuerto Barcelona
        ]
        
        cls.airspace.navsegments = [
            NavSegment(1, 2, 109.631114),  # GIR -> GODOX
            NavSegment(2, 3, 53.803332),    # GODOX -> GRAUS
            NavSegment(3, 1, 32.925622),    # GRAUS -> GIR
            NavSegment(4, 1, 48.55701)      # IZA -> GIR
        ]
        
        cls.airspace.navairports = [
            NavAirport("LEBL", [cls.airspace.navpoints[4]], [cls.airspace.navpoints[0]]),
            NavAirport("LEIB", [cls.airspace.navpoints[3]], [])
        ]
        
        # Establecer vecinos manualmente para las pruebas
        cls.airspace.navpoints[0].neighbors = [cls.airspace.navpoints[1]]  # GIR -> GODOX
        cls.airspace.navpoints[1].neighbors = [cls.airspace.navpoints[2]]  # GODOX -> GRAUS
        cls.airspace.navpoints[2].neighbors = [cls.airspace.navpoints[0]]  # GRAUS -> GIR
        cls.airspace.navpoints[3].neighbors = [cls.airspace.navpoints[0]]  # IZA -> GIR

    def test_load_navpoints(self):
        """Prueba la carga de puntos de navegación"""
        test_airspace = AirSpace()
        test_airspace.load_navpoints()
        self.assertGreater(len(test_airspace.navpoints), 0)
        self.assertIsInstance(test_airspace.navpoints[0], NavPoint)

    def test_load_navsegments(self):
        """Prueba la carga de segmentos"""
        test_airspace = AirSpace()
        test_airspace.load_navpoints()
        test_airspace.load_navsegments()
        self.assertGreater(len(test_airspace.navsegments), 0)
        self.assertIsInstance(test_airspace.navsegments[0], NavSegment)
        
        # Verificar que se establecieron las relaciones de vecinos
        for point in test_airspace.navpoints:
            for seg in test_airspace.navsegments:
                if seg.origin_number == point.number:
                    neighbor = next((p for p in test_airspace.navpoints 
                                   if p.number == seg.destination_number), None)
                    self.assertIn(neighbor, point.neighbors)

    def test_load_navairports(self):
        """Prueba la carga de aeropuertos"""
        test_airspace = AirSpace()
        test_airspace.load_navpoints()
        test_airspace.load_navairports()
        self.assertGreater(len(test_airspace.navairports), 0)
        self.assertIsInstance(test_airspace.navairports[0], NavAirport)
        
        # Verificar que los SIDs y STARs son NavPoints válidos
        for airport in test_airspace.navairports:
            for sid in airport.sids:
                self.assertIsInstance(sid, NavPoint)
            for star in airport.stars:
                self.assertIsInstance(star, NavPoint)

    def test_reachability(self):
        """Prueba la función de alcance"""
        from airspace import ReachabilityAirspace
        
        # Desde GIR debería alcanzar GODOX, GRAUS y de vuelta a GIR
        reachable = ReachabilityAirspace(self.airspace, "GIR")
        self.assertEqual(len(reachable), 3)
        self.assertIn(self.airspace.navpoints[0], reachable)  # GIR
        self.assertIn(self.airspace.navpoints[1], reachable)  # GODOX
        self.assertIn(self.airspace.navpoints[2], reachable)  # GRAUS
        
        # Desde IZA debería alcanzar GIR, GODOX y GRAUS
        reachable = ReachabilityAirspace(self.airspace, "IZA")
        self.assertEqual(len(reachable), 4)

    def test_shortest_path(self):
        """Prueba la función de camino más corto"""
        from airspace import FindShortestPathAirspace
        
        # Camino directo GIR -> GODOX
        path = FindShortestPathAirspace(self.airspace, "GIR", "GODOX")
        self.assertEqual(len(path.nodes), 2)
        self.assertEqual(path.nodes[0].name, "GIR")
        self.assertEqual(path.nodes[1].name, "GODOX")
        self.assertAlmostEqual(path.cost, 109.631114, places=5)
        
        # Camino con múltiples segmentos GIR -> GODOX -> GRAUS
        path = FindShortestPathAirspace(self.airspace, "GIR", "GRAUS")
        self.assertEqual(len(path.nodes), 3)
        self.assertEqual(path.nodes[0].name, "GIR")
        self.assertEqual(path.nodes[1].name, "GODOX")
        self.assertEqual(path.nodes[2].name, "GRAUS")
        self.assertAlmostEqual(path.cost, 109.631114 + 53.803332, places=5)
        
        # Camino circular GRAUS -> GIR -> GODOX
        path = FindShortestPathAirspace(self.airspace, "GRAUS", "GODOX")
        self.assertEqual(len(path.nodes), 3)
        self.assertEqual(path.nodes[0].name, "GRAUS")
        self.assertEqual(path.nodes[1].name, "GIR")
        self.assertEqual(path.nodes[2].name, "GODOX")
        self.assertAlmostEqual(path.cost, 32.925622 + 109.631114, places=5)
        
        # Camino desde aeropuerto (LEBL) a punto de navegación
        path = FindShortestPathAirspace(self.airspace, "LEBL", "GIR")
        self.assertEqual(len(path.nodes), 2)
        self.assertEqual(path.nodes[0].name, "LEBL")
        self.assertEqual(path.nodes[1].name, "GIR")

    def test_no_path(self):
        """Prueba cuando no hay camino disponible"""
        from airspace import FindShortestPathAirspace
        
        # No hay camino de vuelta desde IZA a LEBL en estos datos de prueba
        path = FindShortestPathAirspace(self.airspace, "IZA", "LEBL")
        self.assertIsNone(path)

    def test_plot_functions(self):
        """Prueba que las funciones de graficación no fallen"""
        from airspace import PlotAirspace, PlotReachabilityAirspace
        
        # Prueba PlotAirspace
        fig = PlotAirspace(self.airspace)
        self.assertIsNotNone(fig)
        
        # Prueba PlotReachabilityAirspace
        reachable = ReachabilityAirspace(self.airspace, "GIR")
        fig = PlotReachabilityAirspace(self.airspace, reachable)
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()