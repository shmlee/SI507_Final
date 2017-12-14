import unittest
from SI507F17_finalproject import *


class test_Fonts(unittest.TestCase):
	def setUp(self):
		pass
	def test_constructor_Font(self):
		x = Font("Open Sans", "Open Sans", 8)
		self.assertEqual(type(x.font_name), type(""))
	def test_constructor_Font2(self):
		x = Font("Open Sans", "Open Sans", 8)
		self.assertEqual(type(x.img), type(""))
	def test_constructor_Font3(self):
		x = Font("Open Sans", "Open Sans", 8)
		self.assertEqual(type(x.font_style), int)


class test_Top_fonts(unittest.TestCase):
	def test_Top_fonts(self):
		self.top_fonts = Top_fonts()
		for top_object in self.top_fonts.hot_fonts:
			self.assertIsInstance(top_object, Font)
	def test_Top_fonts2(self):
		self.top_fonts = Top_fonts()
		for popular_object in self.top_fonts.popular_fonts:
			self.assertIsInstance(popular_object, Font)
	def test_Top_fonts_type(self):
		self.top_fonts = Top_fonts()
		self.assertEqual(type(self.top_fonts.hot_fonts), type([]))
	def test_Top_fonts_type2(self):	
		self.top_fonts = Top_fonts()
		self.assertEqual(type(self.top_fonts.popular_fonts), type([]))

class test_list_vars(unittest.TestCase):

	def test_assertIsInstance(self):
		self.assertIsInstance(three_fonts,list)
		self.assertIsInstance(fonts_obj,list)
		self.assertIsInstance(fonts_obj2,list)

	def test_list_elem_types(self):
		self.assertIsInstance(fonts_obj[0],Font)
		self.assertIsInstance(fonts_obj2[0],Font)

	





		



		








if __name__ == "__main__":
	unittest.main(verbosity=2)