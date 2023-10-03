from __future__ import annotations

import abc
import typing

import pygame

from Config import Config
from TemplateTile import TileType

if typing.TYPE_CHECKING:
    from Tile import Tile


class TileRepresenter:
    def __init__(self, tile: Tile, kwargs):
        self.tile = tile
        self.kwargs = kwargs

    @abc.abstractmethod
    def draw(self, screen: pygame.Surface):
        raise NotImplemented()


class LineRepresenter(TileRepresenter):
    def draw(self, screen: pygame.Surface):
        actual_x = self.tile.x * Config.CW
        actual_y = self.tile.y * Config.CH

        if self.tile.template_tile.rotation == 0:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
            )
        elif self.tile.template_tile.rotation == 1:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (actual_x + Config.CW // 4, actual_y, Config.CW // 2, Config.CH)
            )


class CornerRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        if self.tile.template_tile.rotation == 0:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                    Config.CW // 2,
                    Config.CH // 2 + Config.CH // 4
                )
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW // 2 + Config.CW // 4 + 1,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 1:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                    Config.CW // 2,
                    Config.CH // 2 + Config.CH // 4
                )
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW // 2 + Config.CW // 4,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 2:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH,
                    Config.CW // 2,
                    Config.CH // 2
                )
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW - 1,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 3:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH,
                    Config.CW // 2,
                    Config.CH // 2
                )
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )


class CrossRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
        )


class ForkRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        if self.tile.template_tile.rotation == 0:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 1:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                    Config.CW // 2,
                    Config.CH // 2 + Config.CH // 4
                )
            )
        elif self.tile.template_tile.rotation == 2:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW - 1,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 3:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
            )

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH,
                    Config.CW // 2,
                    Config.CH // 2
                )
            )


class DeadEndRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        if self.tile.template_tile.rotation == 0:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                    Config.CW // 2,
                    Config.CH // 2 + Config.CH // 4
                )
            )
        elif self.tile.template_tile.rotation == 1:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW - 1,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 2:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH,
                    Config.CW // 2,
                    Config.CH // 2
                )
            )
        elif self.tile.template_tile.rotation == 3:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    self.tile.x * Config.CW + Config.CW // 4,
                    self.tile.y * Config.CH + Config.CH // 4,
                    Config.CW - Config.CW // 4,
                    Config.CH // 2
                )
            )


class EmptyRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pass


class GenericBoxPlaceholder(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (self.kwargs["color"]),
            (self.tile.x * Config.CW, self.tile.y * Config.CH, Config.CW, Config.CH)
        )


class TileRepresenterBuilder:
    representer_mapping = {
        TileType.LINE: LineRepresenter,
        TileType.CROSS: CrossRepresenter,
        TileType.CORNER: CornerRepresenter,
        TileType.DEAD_END: DeadEndRepresenter,
        TileType.FORK: ForkRepresenter,
        TileType.SPECIAL_EMPTY: EmptyRepresenter,
        TileType.SPECIAL_SINGLE_ROOM: (GenericBoxPlaceholder, (255, 0, 0)),
        TileType.SPECIAL_BIG_ROOM_ENTRANCE: (GenericBoxPlaceholder, (0, 255, 0)),
        TileType.SPECIAL_BIG_ROOM_MAIN: (GenericBoxPlaceholder, (0, 0, 255)),
        TileType.SPECIAL_BIG_ROOM_WALL: (GenericBoxPlaceholder, (122, 122, 122)),
        TileType.SPECIAL_BIG_ROOM_CORNER: (GenericBoxPlaceholder, (20, 20, 20))
    }

    @classmethod
    def from_tile(cls, tile: Tile) -> TileRepresenter:
        representer = cls.representer_mapping[tile.template_tile.tile_type]
        kwargs = {}

        if type(representer) == tuple:
            kwargs = {"color": representer[1]}
            representer = representer[0]

        return representer(tile, kwargs=kwargs)
