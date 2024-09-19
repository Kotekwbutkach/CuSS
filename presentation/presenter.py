import pygame

from util.color_helper import ColorHelper
from data.aliases import *


class Presenter:
    step: int
    max_step: int

    trajectories: list[tuple[np.ndarray[float], pygame.Color]]
    surface: pygame.surface
    screen_size: PointInt

    view_boundary: BoundaryInt
    position_boundary: NullableBoundaryFloat
    minor_grid: int
    major_grid: int

    trace_length: int

    def __init__(
            self,
            trajectories: list[tuple[np.ndarray[float], pygame.Color]],
            bounds: BoundaryInt = None,
            max_step: int = None,
            margin: int = 15,
            minor_grid: int = 20,
            major_grid: int = 100,
            screen_size: PointInt = (800, 600),
            trace_length: int = 200,
            velocity_length: float = 1.5):
        self.step = 0
        self.max_step = trajectories[0][0].shape[3] - 1 if max_step is None else max_step
        self.trajectories = trajectories

        self.margin = margin
        self.screen_size = screen_size
        self.view_boundary = ((margin, margin), (screen_size[0] - margin, screen_size[1] - margin))
        self.minor_grid = minor_grid
        self.major_grid = major_grid
        pygame.init()
        pygame.display.set_mode(screen_size)
        self.surface = pygame.display.get_surface()
        pygame.display.set_caption('CoDyS')

        if bounds is not None:
            self.position_boundary = bounds
        else:
            self.position_boundary = ((None, None), (None, None))
            self.get_boundaries()

        self.trace_length = trace_length
        self.velocity_length = velocity_length

    def get_boundaries(self):
        for traj, _ in self.trajectories:
            bounds = [np.min(traj, axis=(1, 3)), np.max(traj, axis=(1, 3))]
            position_boundary_0 = (
                tuple(
                    bounds[0][0][j] + bounds[0][1][j]
                    if self.position_boundary[0][j] is None
                    or self.position_boundary[0][j] > bounds[0][0][j]
                    else self.position_boundary[0][j]
                    for j in [0, 1]))
            position_boundary_1 = (
                tuple(
                    bounds[1][0][j] + bounds[1][1][j]
                    if self.position_boundary[1][j] is None
                    or self.position_boundary[1][j] < bounds[1][0][j]
                    else self.position_boundary[1][j]
                    for j in [0, 1]))
            self.position_boundary = (position_boundary_0, position_boundary_1)
        half_width = (self.position_boundary[1][0] - self.position_boundary[0][0]) / 2
        half_height = (self.position_boundary[1][1] - self.position_boundary[0][1]) / 2
        midpoint = tuple((self.position_boundary[1][i] + self.position_boundary[0][i]) / 2 for i in range(2))
        if half_width * self.screen_size[1] > half_height * self.screen_size[0]:
            half_height = half_width * self.screen_size[1] / self.screen_size[0]
        else:
            half_width = half_height * self.screen_size[0] / self.screen_size[1]
        self.position_boundary = (
            (int((midpoint[0] - half_width) / self.minor_grid - 1) * self.minor_grid,
             int((midpoint[1] - half_height) / self.minor_grid - 1) * self.minor_grid),
            ((int((midpoint[0] + half_width) / self.minor_grid) + 1) * self.minor_grid,
             (int((midpoint[1] + half_height) / self.minor_grid) + 1) * self.minor_grid))

    def mtv_translate(self, position: PointFloat) -> PointFloat:
        fraction = [(position[i] - self.position_boundary[0][i])
                    / (self.position_boundary[1][i] - self.position_boundary[0][i]) for i in range(2)]

        view_position = tuple(
            self.view_boundary[0][i]
            + (self.view_boundary[1][i] - self.view_boundary[0][i])
            * fraction[i] for i in range(2))
        return view_position

    def draw_bounds(self):
        origin = self.mtv_translate(self.position_boundary[0])
        size = tuple(
            self.mtv_translate(self.position_boundary[1])[i]
            - self.mtv_translate(self.position_boundary[0])[i]
            for i in range(2))
        pygame.draw.rect(
            self.surface,
            pygame.Color("white"),
            pygame.Rect(*origin, *size),
            1
        )

    def _get_grid_lines(self, origin: PointInt, end: PointInt, grid_diam):
        return (
            [(
                (self.position_boundary[0][0], origin[1] + (k+1) * grid_diam),
                (self.position_boundary[1][0], origin[1] + (k+1) * grid_diam))
                for k in range((end[1] - origin[1]) // grid_diam)]
            + [(
                (origin[0] + (k+1) * grid_diam, self.position_boundary[0][1]),
                (origin[0] + (k+1) * grid_diam, self.position_boundary[1][1]))
                for k in range((end[0] - origin[0]) // grid_diam)])

    def _draw_lines(self, lines, color: pygame.Color):
        for line_start, line_end in lines:
            pygame.draw.line(
                self.surface,
                pygame.Color(color),
                self.mtv_translate(line_start),
                self.mtv_translate(line_end))

    def draw_grid(self):
        origin = (
            int(self.position_boundary[0][0]/self.minor_grid) * self.minor_grid,
            int(self.position_boundary[0][1]/self.minor_grid) * self.minor_grid)
        end = (
            int(self.position_boundary[1][0]/self.minor_grid) * self.minor_grid,
            int(self.position_boundary[1][1]/self.minor_grid) * self.minor_grid)
        minor_lines = self._get_grid_lines(origin, end, self.minor_grid)
        self._draw_lines(minor_lines, pygame.Color("Gray40"))
        major_lines = self._get_grid_lines(origin, end, self.major_grid)
        self._draw_lines(major_lines, pygame.Color("Gray60"))

    def draw_trajectories(self):
        for traj, color in self.trajectories:
            for i in range(traj.shape[1]):
                pygame.draw.circle(
                    self.surface,
                    color,
                    self.mtv_translate((traj[0, i, 0, self.step], traj[0, i, 1, self.step])),
                    5)

    def draw_velocities(self):
        for traj, color in self.trajectories:
            for i in range(traj.shape[1]):
                pygame.draw.line(
                    self.surface,
                    ColorHelper.mix(color, pygame.Color("white"), 1, 1),
                    self.mtv_translate((traj[0, i, 0, self.step], traj[0, i, 1, self.step])),
                    self.mtv_translate((traj[0, i, 0, self.step] + self.velocity_length * traj[1, i, 0, self.step],
                                        traj[0, i, 1, self.step] + self.velocity_length * traj[1, i, 1, self.step])),
                    3)

    def draw_traces(self):
        trace_start = max(0, self.step - self.trace_length)
        for traj, color in self.trajectories:
            for i in range(traj.shape[1]):
                for s in range(trace_start, self.step):
                    current_color = ColorHelper.mix(color,
                                                    pygame.Color("black"),
                                                    s - trace_start,
                                                    self.step - trace_start)
                    current_size = (3 * s) / self.step
                    pygame.draw.circle(
                        self.surface,
                        current_color,
                        self.mtv_translate((traj[0, i, 0, s], traj[0, i, 1, s])),
                        current_size)

    def draw_step(self):
        self.surface.fill(pygame.Color("black"))
        self.draw_grid()
        self.draw_bounds()
        if self.trace_length > 0:
            self.draw_traces()
        self.draw_trajectories()
        if self.velocity_length > 0:
            self.draw_velocities()

        pygame.display.flip()

    def present(self):
        self.draw_step()

        clock = pygame.time.Clock()
        running = True
        started = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        started = True
            if started:
                self.draw_step()
                if self.step < self.max_step:
                    self.step += 1
                clock.tick(120)
