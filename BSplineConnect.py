import numpy as np
from scipy.interpolate import BSpline
import matplotlib.pyplot as plt

def create_open_uniform_nodes(num_control_points, degree):
    nodes = np.zeros(num_control_points + degree + 1)
    nodes[:degree + 1] = 0
    nodes[-degree - 1:] = num_control_points - degree
    nodes[degree + 1:-degree - 1] = np.arange(1, num_control_points - degree)
    return nodes

def merge_bspline_segments(P, U, Q, V, degree):
    """
    Merge two B-spline segments' control points and knot vectors to ensure consistent length.

    Parameters:
    - P: Control points of the first B-spline segment
    - U: Knot vector of the first B-spline segment
    - Q: Control points of the second B-spline segment
    - V: Knot vector of the second B-spline segment
    - degree: Degree of the B-spline

    Returns:
    - Merged knot vector and control points
    """
    # Ensure positional continuity
    if not np.allclose(P[-1], Q[0]):
        # Adjust the first control point of Q to ensure positional continuity
        Q[0] = P[-1]

    # Adjust the first control point of the second B-spline to ensure first-order derivative continuity
    Q[1] = 2 * Q[0] - P[-2]

    # Merge control points
    control_points = np.vstack((P, Q[1:]))

    V += U[-1]
    # Merge knot vectors
    U_prime = np.concatenate((U[:-degree], V[degree - 1:]))

    # Ensure the length of the knot vector matches the number of control points and degree
    expected_knots_length = len(control_points) + degree + 1
    if len(U_prime) != expected_knots_length:
        raise ValueError("Knots, control points, and degree are inconsistent")

    return U_prime, control_points

# Example usage
degree = 3
P = np.array([[0, 0], [1, 2], [2, 2], [3, 0], [4, 2]])
U = create_open_uniform_nodes(len(P), degree)
print("U:", U)

Q = np.array([[4, 0], [4, -1], [5, -2], [6, 0], [7, 4]])
V = create_open_uniform_nodes(len(Q), degree)
print("V:", V)

# Create the individual B-splines
spline1 = BSpline(U, P, degree)
spline2 = BSpline(V, Q, degree)


# Plot the B-splines
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
# Plot the individual B-splines
t1 = np.linspace(U[degree], U[-degree - 1], 200)
points1 = spline1(t1)
axs[0].plot(points1[:, 0], points1[:, 1], 'b-', label='B-Spline 1')
axs[0].plot(P[:, 0], P[:, 1], 'ro-', label='Control Points 1')

t2 = np.linspace(V[degree], V[-degree - 1], 200)
points2 = spline2(t2)
axs[0].plot(points2[:, 0], points2[:, 1], 'g-', label='B-Spline 2')
axs[0].plot(Q[:, 0], Q[:, 1], 'mo-', label='Control Points 2')

U_prime, control_points = merge_bspline_segments(P, U, Q, V, degree)
# Create the merged B-spline
spline_merged = BSpline(U_prime, control_points, degree)

axs[0].legend()
axs[0].set_xlabel('x')
axs[0].set_ylabel('y')
axs[0].set_title('Individual B-Spline Curves')

# Plot the merged B-spline
t_merged = np.linspace(U_prime[degree], U_prime[-degree - 1], 400)
points_merged = spline_merged(t_merged)
axs[1].plot(points_merged[:, 0], points_merged[:, 1], 'b-', label='Merged B-Spline')
axs[1].plot(control_points[:, 0], control_points[:, 1], 'ro-', label='Control Points')

axs[1].legend()
axs[1].set_xlabel('x')
axs[1].set_ylabel('y')
axs[1].set_title('Merged B-Spline Curve')

plt.tight_layout()
plt.show()
