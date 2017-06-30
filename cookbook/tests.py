from django.test import TestCase
from cookbook.models import Recette

class RecetteTest(TestCase):

    def test_recette_existe(self):
        pomme = Recette.objects.get(titre="Pommes sur île flottante")
        pomme.save()
        self.assertEqual(pomme.titre, "Pommes sur île flottante")
        self.assertEqual(pomme.type, "D")
        self.assertEqual(pomme.difficulte, 1)
        self.assertEqual(pomme.cout, 10)
        self.assertEqual(pomme.temps_prepa, 10)
        self.assertEqual(pomme.temps_cuisson, 10)
        self.assertEqual(pomme.temps_repos, 0)




