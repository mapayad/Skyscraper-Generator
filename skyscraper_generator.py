"""A python script used in Maya that generates random skyscrapers."""
# Marie Payad
# ASWF 2022
# skyscraper_generator.py

from __future__ import print_function
import math
import random
from datetime import datetime
from this import s
from maya import cmds

random.seed(datetime.now())


class SkyscraperGeneratorUI:
    """This class creates the UI Window."""

    def __init__(self):
        self.window_id = 'SkyscraperWindow'
        # Checks if the UI window already exist and closes it
        if cmds.window(self.window_id, exists=True):
            cmds.deleteUI(self.window_id)
        # Opens a new UI window
        self.window = cmds.window(
            self.window_id, title='Random Skyscraper Generator', resizeToFitChildren=True)
        cmds.row_column_layout(
            number_of_columns=3,
            column_width=[(1, 125), (2, 115), (3, 50)],
            column_offset=[(1, 'right', 3)])

        # Extra spacing in the UI window for better formatting
        cmds.separator(h=15, style='none')
        cmds.separator(h=15, style='none')
        cmds.separator(h=15, style='none')

        # Sets the Foundation Dimensions
        cmds.text(label='Foundation Width')
        self.foundation_width = cmds.intField(min_value=5, max_value=25, value=10)
        cmds.separator(h=10, style='none')
        cmds.text(label='Foundation Height')
        self.foundation_height = cmds.intField(min_value=5, max_value=25, value=10)
        cmds.separator(h=10, style='none')

        # Extra spacing in the UI window for better formatting
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')

        # Creates the UI button for generating the Foundation
        cmds.separator(h=15, style='none')
        cmds.button(label="Create Foundation", command=self.plane_specs)
        cmds.separator(h=15, style='none')

        # Extra spacing in the UI window for better formatting
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')

        # Sets the Skyscraper Dimensions
        cmds.text(label='Skyscraper Height')
        self.skyscraper_height = cmds.intField(min_value=0, max_value=10, value=8)
        cmds.separator(h=10, style='none')
        cmds.text(label='Skyscraper Base')
        self.skyscraper_margin = cmds.intField(minValue=0, maxValue=10, value=10)
        cmds.separator(h=10, style='none')

        # Extra spacing in the UI window for better formatting
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')
        cmds.separator(h=10, style='none')

        # Creates the UI button for clearing the Foundation and generating the Skyscrapers
        cmds.button(label="Empty Foundation", command=delete_skyscrapers)
        cmds.button(label="Create Skyscrapers", command=self.foundation_specs)
        cmds.separator(h=15, style='none')

        # Extra spacing in the UI window for better formatting
        cmds.separator(h=15, style='none')
        cmds.separator(h=15, style='none')
        cmds.separator(h=15, style='none')

        # Displays the UI window
        cmds.showWindow()

    def plane_specs(self):
        """This function specifies the plane dimensions."""
        foundation_width = cmds.intField(self.foundation_width, query=True, value=True)
        foundation_height = cmds.intField(self.foundation_height, query=True, value=True)
        print(foundation_width, foundation_height)
        # Calls the function to create the plane
        create_plane(foundation_width, foundation_height)

    def foundation_specs(self):
        """This function specifies the foundation dimensions."""
        foundation_width = cmds.intField(self.foundation_width, query=True, value=True)
        foundation_height = cmds.intField(self.foundation_height, query=True, value=True)
        skyscraper_height = cmds.intField(self.skyscraper_height, query=True, value=True)
        skyscraper_margin = cmds.intField(self.skyscraper_margin, query=True, value=True)
        print(foundation_width, foundation_height, skyscraper_height, skyscraper_margin)
        # Calls the function to create the foundation
        create_foundation(foundation_width, foundation_height, skyscraper_height, skyscraper_margin)


def delete_plane(name):
    """This function deletes the base plane."""
    if cmds.objExists(name):
        cmds.delete(name)


def create_plane(width, height):
    """This function generates the base plane."""
    delete_plane('base_plane')
    delete_plane('original_base_plane')
    # Creates the base plane dimensions
    cmds.polyPlane(
        side_x=width * 2,
        side_y=height * 2,
        w=width,
        h=height,
        name='original_base_plane')
    # Empties the existing skyscrapers
    delete_skyscrapers()


def copy_plane():
    """This function copies the base plane."""
    cmds.showHidden('original_base_plane')
    cmds.duplicate('original_base_plane', name='base_plane')
    cmds.hide('original_base_plane')


def delete_skyscrapers():
    """This function deletes the existing skyscrapers."""
    skyscrapers = cmds.ls('plane_skyscraper*')
    if len(skyscrapers) > 0:
        cmds.delete(skyscrapers)


def create_foundation(width, height, max_height, spacing_intensity):
    """This function generates the Foundation."""

    # Deletes the existing skyscrapers
    delete_skyscrapers()
    delete_plane('base_plane')

    # Copies the base plane in case of modification
    copy_plane()

    # Calculates the number of vertices for the placement of the skyscrapers
    vertices_number = (width * 2 + 1) * (height * 2 + 1)
    print(vertices_number)

    # Calculates the number of skyscrapers
    skyscrapers_number = int(math.ceil(vertices_number / 2.0))
    print(skyscrapers_number)

    # Calculates the number of faces
    faces_number = (width * 2) * (height * 2)
    print(faces_number)
    max_width = spacing_intensity / 10.0
    max_depth = max_width
    odd_row = width + 1
    even_row = width * 2 + 1
    if width > height:
        max_dimension = width
    else:
        max_dimension = height
    base_height = 0.25

    # Extrudes the base plane
    cmds.select('base_plane*')
    cmds.polyExtrudeFacet(localTranslateZ=base_height)

    # Adds a locator to the center of each skyscraper quadrant
    for i in range(0, vertices_number):
        # Skips every other row of vertices and every other vertices of those selected rows
        if (i % 2) == 0:
            x_axis, y_axis, z_axis = cmds.xform(
                f'basePlane*.vtx{s}]' % i,
                query=True,
                t=True,
                worldspace=True)
            # Randomly determines the height of the skyscraper within a range
            current_skyscraper_height = random.randint(1, max_height)
            # Creates and places a new skyscraper
            current_skyscraper = cmds.polyCube(
                side_x=4,
                side_y=current_skyscraper_height * 5,
                side_z=4,
                weight=max_width,
                height=current_skyscraper_height,
                depth=max_depth,
                name='skyscraper#')
            cmds.move(
                x_axis,
                y_axis + current_skyscraper_height / 2.0 + base_height,
                z_axis,
                current_skyscraper)

    # Deletes the existing skyscrapers that are not on specified vertices on the grid
    for j in range(1, skyscrapers_number + 1):
        if j <= odd_row:
            cmds.delete(f'skyscraper{s}' % j)
        for k in range(1, max_dimension + 1):
            if j > k * even_row <= k * even_row + odd_row:
                cmds.delete(f'skyscraper{s}' % j)
        # Renames the skyscrapers
        if cmds.objExists(f'skyscraper{s}' % j):
            cmds.rename(f'skyscraper{s}' % j, 'planeSkyscraper')
    cmds.rename('planeSkyscraper', 'planeSkyscraper0')

    # Selects blocks across the width
    width_step = (width * 2) * 2
    random_block_start = random.randrange(0, faces_number, width_step)
    print(random_block_start)
    for side_a in range(0, faces_number):
        if side_a >= random_block_start < random_block_start + width_step:
            cmds.select(f'basePlane*.f{s}' % side_a, add=True)
    skyscrapers_full_number = width * height
    skyscraper_row_number = random_block_start / width_step
    print(skyscraper_row_number)
    for side_b in range(0, skyscrapers_full_number):
        if side_b >= skyscraper_row_number * width < skyscraper_row_number * width + width:
            if cmds.objExists(f'planeSkyscraper{s}' % side_b):
                cmds.delete(f'planeSkyscraper{s}' % side_b)

    # Selects blocks across the height
    height_step = 2
    random_block_start = random.randrange(0, width * 2, height_step)
    print(random_block_start)
    for side_a in range(0, faces_number):
        if ((side_a % (width_step / 2)) == random_block_start) \
                or ((side_a % (width_step / 2)) == (random_block_start + 1)):
            cmds.select(f'basePlane*.f{s}' % side_a, add=True)
    skyscraper_column_number = random_block_start / height_step
    print(skyscraper_column_number)
    for side_b in range(0, skyscrapers_full_number):
        if (side_b % width) == skyscraper_column_number:
            if cmds.objExists(f'planeSkyscraper{s}' % side_b):
                cmds.delete(f'planeSkyscraper{s}' % side_b)

    # Extrudes the block
    cmds.polyExtrudeFacet(offset=0.1, localTranslateZ=- (base_height - (base_height / 5)))


# Calls the UI
window = SkyscraperGeneratorUI()
