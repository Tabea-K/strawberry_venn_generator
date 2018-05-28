from unittest import TestCase
import strawberry_venn_generator


class TestSvgContent(TestCase):

    def test_is_svg(self):
        svg = strawberry_venn_generator.import_empty_venn_svg()
        self.assertEqual(svg.split()[0], "<?xml")
        self.assertEqual(svg.split()[-1], "</svg>")


class TestReadFiles(TestCase):
    def get_data(self):
        from os import path
        file1 = open(path.join(path.dirname(__file__), 'test_files', 'file1.txt'), 'r')
        file2 = open(path.join(path.dirname(__file__), 'test_files', 'file2.txt'), 'r')
        file3 = open(path.join(path.dirname(__file__), 'test_files', 'file3.txt'), 'r')
        data = strawberry_venn_generator.read_files([file1, file2, file3])
        return data

    def test_read_test_files(self):
        data = self.get_data()
        self.assertEqual(len(data),3)

class TestVennNumbers(TestCase):

    def get_data(self):
        from os import path
        file1 = open(path.join(path.dirname(__file__), 'test_files', 'file1.txt'), 'r')
        file2 = open(path.join(path.dirname(__file__), 'test_files', 'file2.txt'), 'r')
        file3 = open(path.join(path.dirname(__file__), 'test_files', 'file3.txt'), 'r')
        data = strawberry_venn_generator.read_files([file1, file2, file3])
        return data

    def test_intersection_of_all(self):
        data = self.get_data()
        self.assertEqual(strawberry_venn_generator.get_intersection_of_all_three(data), 4)

    def test_intersection_of_two(self):
        data = self.get_data()
        self.assertEqual(strawberry_venn_generator.get_intersection_of_two_sets(data, [0,1]), 6)

    def test_unique_for_a_set(self):
        data = self.get_data()
        self.assertEqual(strawberry_venn_generator.get_unique_for_a_set(data, 0), 5)


class TestOutputFile(TestCase):

    def get_data(self):
        from os import path
        file1 = open(path.join(path.dirname(__file__), 'test_files', 'file1.txt'), 'r')
        file2 = open(path.join(path.dirname(__file__), 'test_files', 'file2.txt'), 'r')
        file3 = open(path.join(path.dirname(__file__), 'test_files', 'file3.txt'), 'r')
        data = strawberry_venn_generator.read_files([file1, file2, file3])
        return data

    def test_svg_output(self):
        from os import path

        data = self.get_data()
        empty_venn = strawberry_venn_generator.import_empty_venn_svg()
        correct_venn_filepath = path.join(path.dirname(__file__), 'test_files', 'correct_venn_diagram.svg')

        with open(correct_venn_filepath, 'r') as correct_venn_filehandle:
            correct_venn_svg = correct_venn_filehandle.read()
        test_venn = strawberry_venn_generator.get_svg_diagram_content(empty_venn,
                                                                      data,
                                                                      ["f1", "f2", "f3"],
                                                                      "venn_title")
        self.assertEqual(correct_venn_svg, test_venn)
