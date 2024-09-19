import numpy as np


class Analyst:
    @staticmethod
    def analyze_single(trajectory: np.ndarray):
        number_of_particles = trajectory.shape[1]

        position = trajectory[0, :]
        velocity = trajectory[1, :]

        position_distance = (
                np.tile(position, (number_of_particles, 1, 1, 1))
                - np.tile(position, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
        particle_position_distance = np.sqrt(np.sum(position_distance ** 2, axis=2))

        min_of_position_distances = np.sort(np.sort(particle_position_distance, axis=1), axis=0)[0, 1, :]
        mean_of_position_distances = (np.mean(particle_position_distance, axis=(0, 1))
                                      * number_of_particles / (number_of_particles - 1))
        max_of_position_distances = np.max(particle_position_distance, axis=(0, 1))
        std_of_position_distances = np.std(particle_position_distance, axis=(0, 1))

        velocity_distance = (
                np.tile(velocity, (number_of_particles, 1, 1, 1))
                - np.tile(velocity, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
        particle_velocity_distance = np.sqrt(np.sum(velocity_distance ** 2, axis=2))

        min_of_velocity_distances = np.sort(np.sort(particle_velocity_distance, axis=1), axis=0)[0, 1, :]
        mean_of_velocity_distances = (np.mean(particle_velocity_distance, axis=(0, 1))
                                      * number_of_particles / (number_of_particles - 1))
        max_of_velocity_distances = np.max(particle_velocity_distance, axis=(0, 1))
        std_of_velocity_distances = np.std(particle_velocity_distance, axis=(0, 1))

        distance_results = [
            min_of_position_distances,
            mean_of_position_distances,
            max_of_position_distances,
            std_of_position_distances]
        velocity_results = [
            min_of_velocity_distances,
            mean_of_velocity_distances,
            max_of_velocity_distances,
            std_of_velocity_distances]
        return np.array([distance_results, velocity_results])

    @staticmethod
    def analyze(trajectories: list[np.ndarray]):
        separate_results = list()
        for traj in trajectories:
            separate_results.append(Analyst.analyze_single(traj))
        grouped_results = np.array(separate_results)
        average_results = np.mean(grouped_results, axis=0)
        return average_results
