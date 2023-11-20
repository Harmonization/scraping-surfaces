import plotly.graph_objs as go

def surface_3d(points):
        # Визуализация поверхности (должна открыться вкладка в браузере)
        fig_3d = go.Figure()
        
        x = list(points[:, 0])
        y = list(points[:, 1])
        z = list(points[:, 2])
        if points.shape[1] == 4:
            x *= 2
            y *= 2
            z += list(points[:, 3])
        
        fig_3d.add_trace(
            go.Scatter3d(
                visible=True,
                line=dict(color="#00CED1", width=6),
                name=f"𝜈 = step",
                x=x, y=y, z=z, mode='markers'))
        fig_3d.show()