import unittest
import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Importamos todos tus módulos
from basics import normalize
import caesar
import affine
import monoalpha
import vigenere
from break_caesar import break_caesar
from break_affine import break_affine
from break_vigenere import break_vigenere

class TestCiphers(unittest.TestCase):

    def setUp(self):
        self.plaintext = "HELLOWORLD"
        self.edge_cases = ["", "A", "123!@#", "AB"]
        self.long_text = "MANCHESTERUNITEDFOOTBALLCLUBISAPROFESSIONALFOOTBALLCLUBBASEDINOLDTRAFFORDGREATERMANCHESTERENGLANDTHECLUBCOMPETESINTHEPREMIERLEAGUETHETOPFLIGHTOFENGLISHFOOTBALLNICKNAMEDTHEREDDEVILSTHEYWEREFOUNDEDASNEWTONHEATHLYRFOOTBALLCLUBINEIGHTEENSEVENTYEIGHTBUTCHANGEDTHEIRNAMETOMANCHESTERUNITEDINNINETEENZEROTWOTHECLUBHASWONARECORDTWENTYLEAGUETITLESTWELVEFACUPSSIXLEAGUECUPSANDARECORDTWENTYONEFACOMMUNITYSHIELDSTHEYHAVEWONTHEEUROPEANCUPTHREETIMESANDTHEUEFAEUROPALEAGUETHEUEFACUPWINNERSCUPTHEUEFASUPERCUPTHEINTERCONTINENTALCUPANDTHEFIFACLUBWORLDCUPONCEEACHINNINETEENNNINETYNINETHECLUBACHIEVEDACONTINENTALTREBLEOFTHEPREMIERLEAGUEFACUPANDUEFACHAMPIONSLEAGUEAFIRSTINENGLISHFOOTBALLTHEMUNICHAIRDISASTEROFNINETEENFIFTYEIGHTCLAIMEDTHELIVESOFEIGHTPLAYERSINNINETEENSIXTYEIGHTUNDERTHEMANAGEMENTOFMATTBUSBYTHEYBECAMETHEFIRSTENGLISHFOOTBALLCLUBTOWINTHEEUROPEANCUPSIRALEXFERGUSONISTHECLUBSLONGESTSERVINGANDMOSTSUCCESSFULMANAGERWINNINGTHIRTYEIGHTTROPHIESINCLUDINGTHIRTEENLEAGUETITLESFIVEFACUPSANDTWOCHAMPIONSLEAGUETITLESBETWEENNINETEENEIGHTYSIXANDTWENTYTHIRTEENINTHENINETEENNNINETIESTHECLUBWASFLOATEDONTHELONDONSTOCKEXCHANGEANDWASPURCHASEDBYMALCOLMGLAZERINTWOTHOUSANDANDFIVEATAVALUATIONOFALMOSTEIGHTHUNDREDMILLIONPOUNDSTHECLUBHASPRODUCEDMANYLEGENDARYPLAYERSSUCHASBOBBYCHARLTONGEORGEBESTDENISLAWRYANGIGGSPAULSCHOLESERICCANTONACRISTIANORONALDOANDWAYNEROONEYWHOISTHEALLTIMETOPGOALSCORERFORTHECLUBTHESTADIUMOLDTRAFFORDISOFTENREFERREDTOASTHETHEATREOFDREAMSANDHASACAPACITYOFOVERSEVENTYFOURTHOUSANDSEATSMAKINGITONEOFTHELARGESTSTADIUMSINTHEUNITEDKINGDOM"

    # 1. Round-trip correctness
    def test_round_trip(self):
        # Caesar
        self.assertEqual(caesar.decrypt(caesar.encrypt(self.plaintext, 3), 3), self.plaintext)
        # Affine
        self.assertEqual(affine.decrypt(affine.encrypt(self.plaintext, 5, 8), 5, 8), self.plaintext)
        # Vigenere
        self.assertEqual(vigenere.decrypt(vigenere.encrypt(self.plaintext, "LEMON"), "LEMON"), self.plaintext)
        # Mono
        key = monoalpha.key_from_keyword("CRYPTO")
        self.assertEqual(monoalpha.decrypt(monoalpha.encrypt(self.plaintext, key), key), self.plaintext)

    # 2. Known check values (published in handout)
    def test_known_values(self):
        # Ejemplos que probamos anteriormente
        self.assertEqual(vigenere.encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
        self.assertEqual(monoalpha.encrypt("BOB", "MNBVCXZASDFGHJKLPOIUYTREWQ"), "NKN")

    # 3. Rejection of invalid keys[cite: 4]
    def test_invalid_keys(self):
        with self.assertRaises(ValueError):
            affine.encrypt(self.plaintext, 13, 5) # 13 no es coprimo
        with self.assertRaises(ValueError):
            affine.encrypt(self.plaintext, 2, 5)  # 2 es par
        with self.assertRaises(ValueError):
            vigenere.encrypt(self.plaintext, "LEMON123") # Contiene números
        with self.assertRaises(ValueError):
            monoalpha.encrypt(self.plaintext, "SHORTKEY") # Menos de 26 letras

    # 4. Edge cases[cite: 4]
    def test_edge_cases(self):
        self.assertEqual(caesar.encrypt("", 5), "")
        self.assertEqual(vigenere.encrypt("123!@#", "KEY"), "")
        self.assertEqual(caesar.encrypt("A", 5), "F")
        self.assertEqual(vigenere.decrypt(vigenere.encrypt("HI", "SUPERLONGKEY"), "SUPERLONGKEY"), "HI")


    # 5. Breakers (20 trials reliability)[cite: 4]
    def test_breakers_reliability(self):
        # Caesar (reliable at length 40)
        success_caesar = 0
        for _ in range(20):
            k = random.randint(0, 25)
            cipher = caesar.encrypt(self.long_text[:40], k)
            guessed_k, _ = break_caesar(cipher, "en")
            if guessed_k == k:
                success_caesar += 1
        self.assertEqual(success_caesar, 20) # Debe acertar las 20

        # Affine (reliable at length 60)
        success_affine = 0
        valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        for _ in range(20):
            a, b = random.choice(valid_a), random.randint(0, 25)
            cipher = affine.encrypt(self.long_text[:60], a, b)
            guessed_key, _ = break_affine(cipher, "en")
            if guessed_key == (a, b):
                success_affine += 1
        self.assertEqual(success_affine, 20)

if __name__ == '__main__':
    unittest.main()