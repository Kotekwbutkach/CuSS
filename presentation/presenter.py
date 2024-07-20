import numpy as np
import pygame


class Presenter:
    step: int
    max_step: int

    trajectories: list[tuple[np.ndarray[float], pygame.Color]]
    surface: pygame.surface

    view_boundary: tuple[tuple[int, int], tuple[int, int]]
    position_boundary: tuple[tuple[float | None, float | None], tuple[float | None, float | None]]
    grid_diameter: int

    def __init__(
            self,
            trajectories: list[tuple[np.ndarray[float], pygame.Color]],
            max_step: int = None,
            margin: int = 15):
        self.step = 0
        self.max_step = trajectories[0][0].shape[3] - 1 if max_step is None else max_step
        self.trajectories = trajectories

        self.margin = margin
        screen_size = (800, 600)
        self.view_boundary = ((margin, margin), tuple(screen_size[i] - margin for i in range(2)))
        pygame.init()
        pygame.display.set_mode(screen_size)
        self.surface = pygame.display.get_surface()
        pygame.display.set_caption('CoDyS')

        self.position_boundary = ((None, None), (None, None))
        self.get_boundaries()

    def get_boundaries(self):
        for traj, _ in self.trajectories:
            bounds = [np.min(traj, axis=(1, 3)), np.max(traj, axis=(1, 3))]
            position_boundary_0 = (
                tuple(
                    bounds[0][0][j]
                    if self.position_boundary[0][j] is None
                    or self.position_boundary[0][j] > bounds[0][0][j]
                    else self.position_boundary[0][j]
                    for j in [0, 1]))
            position_boundary_1 = (
                tuple(
                    bounds[1][0][j]
                    if self.position_boundary[1][j] is None
                    or self.position_boundary[1][j] < bounds[1][0][j]
                    else self.position_boundary[1][j]
                    for j in [0, 1]))
            self.position_boundary = (int(position_boundary_0), int(position_boundary_1) + 1)

    def mtv_translate(self, position: tuple[float, float]):
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

    def draw_grid(self):
        grid_minor = 25
        origin = tuple(int(self.position_boundary[0][i]/grid_minor) * grid_minor for i in range(2))
        end = tuple(int(self.position_boundary[1][i]/grid_minor) * grid_minor for i in range(2))
        lines = (
            [(
                (self.position_boundary[0][0], origin[1] + (k+1) * grid_minor),
                (self.position_boundary[1][0], origin[1] + (k+1) * grid_minor))
                for k in range((end[1] - origin[1]) // grid_minor)]
            + [(
                (origin[0] + (k+1) * grid_minor, origin[1]),
                (origin[0] + (k+1) * grid_minor, end[1]))
                for k in range((end[0] - origin[0]) // grid_minor)])
        for line_start, line_end in lines:
            pygame.draw.line(
                self.surface,
                pygame.Color("White"),
                self.mtv_translate(line_start),
                self.mtv_translate(line_end))

    def draw_trajectories(self):
        for traj, color in self.trajectories:
            for i in range(traj.shape[1]):
                pygame.draw.circle(
                    self.surface,
                    color,
                    self.mtv_translate((traj[0, i, 0, self.step], traj[0, i, 1, self.step])),
                    5)

    def draw_step(self):
        self.surface.fill(pygame.Color("black"))
        self.draw_bounds()
        self.draw_grid()
        self.draw_trajectories()
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
