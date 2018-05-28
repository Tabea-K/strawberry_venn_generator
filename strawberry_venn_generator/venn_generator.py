#!/usr/bin/env python
from os import path
import argparse

def import_empty_venn_svg():
    """
    Returns the content of the svg file
    :return: string
    """
    empty_venn_file = path.join(path.dirname(__file__), 'img', 'empty_venn.svg')
    with open(empty_venn_file, "r") as svg_file:
        return svg_file.read()


def get_input_args():
    parser = argparse.ArgumentParser(description="(description follows)")
    parser.add_argument('output_file',
                        help="Name of the venn diagram output file",
                        type=str)
    parser.add_argument('title',
                        help="Title for venn diagram",
                        default="",
                        type=str)
    parser.add_argument('file',
                        help="Files with data to compare",
                        nargs=3,
                        type=argparse.FileType('r'))
    parser.add_argument('name',
                        help="Names to use for the 3 datasets (must be given in the same order as the files!)",
                        nargs=3,
                        type=str)
    args = parser.parse_args()
    return args


def read_files(open_files):
    """
    Returns the contents of the files specified by the user as sets.
    :param open_files: list of three file handlers
    :return: list of three sets
    """
    set_list = []
    for open_file in open_files:
        set_list.append(set(open_file.read().split()))
    return set_list


def get_intersection_of_all_three(set_list):
    """
    Returns the number of lines that are identical between all three sets.
    :param set_list: list of three sets
    :return: int
    """
    return len(set_list[0].intersection(set_list[1].intersection(set_list[2])))


def get_intersection_of_two_sets(set_list, which):
    """
    Returns the number of lines that are identical between two sets.
    :param set_list: list of three sets
    :param which: list of which number of file to compare, i.e. [0,1] for comparing first and second file
    :return: int
    """
    return len(set_list[which[0]].intersection(set_list[which[1]]))


def get_unique_for_a_set(set_list, which):
    """
    Returns the number of lines that are unique for a set.
    :param set_list: list of three sets
    :param which: list for which file to give the number of unique lines
    :return: int
    """
    which_not = list(set([0, 1, 2]) - set([which]))
    return len(set_list[which] - set_list[which_not[0]] - set_list[which_not[1]])


def get_total_length(set_list, which):
    """
    Returns the total length for one dataset.
    :param set_list: list of three sets
    :param which: int for which file to give the number of unique lines
    :return: int
    """
    return len(set_list[which])


def get_svg_diagram_content(empty_venn, set_list, names, title):
    """
    Replaces the names and numbers in the svg file content.
    :param empty_venn: str with content of svg file
    :param set_list: list of three sets
    :param names: the names to be used for the datasets
    :return:
    """
    svg = empty_venn

    # replace name and total count
    svg = svg.replace("A_tot", "%s (%s)" % (names[0], get_total_length(set_list, 0)))
    svg = svg.replace("B_tot", "%s (%s)" % (names[1], get_total_length(set_list, 1)))
    svg = svg.replace("C_tot", "%s (%s)" % (names[2], get_total_length(set_list, 2)))

    # replace unique counts
    svg = svg.replace("A_only", "%s" % (get_unique_for_a_set(set_list, 0)))
    svg = svg.replace("B_only", "%s" % (get_unique_for_a_set(set_list, 1)))
    svg = svg.replace("C_only", "%s" % (get_unique_for_a_set(set_list, 2)))

    # replace intersections between two datasets
    svg = svg.replace("A_B", "%s" % (get_intersection_of_two_sets(set_list, [0, 1])))
    svg = svg.replace("A_C", "%s" % (get_intersection_of_two_sets(set_list, [0, 2])))
    svg = svg.replace("B_C", "%s" % (get_intersection_of_two_sets(set_list, [1, 2])))

    # replace intersections between three datasets
    svg = svg.replace("ABC", "%s" % (get_intersection_of_all_three(set_list)))

    # replace title
    svg = svg.replace("venn_title", "%s" % (title))

    return svg


def write_into_new_svg_file(svg_content, filename):
    with open(filename, 'w') as filehandle:
        filehandle.write(svg_content)


def main():
    empty_venn = import_empty_venn_svg()
    args = get_input_args()
    title = args.title
    set_list = read_files(args.file)
    new_svg = get_svg_diagram_content(empty_venn, set_list, args.name, title)
    write_into_new_svg_file(new_svg, args.output_file)
    print "Wrote new svg file %s!" % args.output_file
