import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="text-align: center">
    <b><font size=6>Txy Calculation Example
        </font></b>
    </div>
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import fsolve

    return fsolve, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Create a $T$-$x$-$y$ diagram for propane/benzene at the bubble point

    ## Bubble point calculation based on Rachford-Rice

    At the bubble point, the Rachford-Rice equation reduces to:
    $\sum_{i=1}^C z_i K_i = 1.$
    In residual form, this can be written as
    $r(T) = 1 - \sum_{i=1}^C z_i K_i$

    Remember that $K_i = f(T,P)$. For a $T$-$x$-$y$ diagram, $P$ is set, so we need to find the value of $T$ for which the above equations are satisfied. That means we'll need to set up an optimization problem to minimize the above equation with respect to $T$.

    Working backwards, we can see that we'll need a way to get $K_i$. So, we'll need a function for Raoult's Law

    $$
    K_i = \frac{P_i^{sat}}{P}
    $$

    Because $P_i^{sat}$ depends on temperature, we'll also need a function for Antoine's equation:

    $$
    P_i^{sat} = 10^{(A - B / ( T + C))}
    $$
    """)
    return


@app.cell
def _():
    from get_antoine_coefficient import get_antoine_coefficient
    from antoine import antoine
    from raoult_law_kvalue import raoult_law_kvalue

    return get_antoine_coefficient, raoult_law_kvalue


@app.cell
def _(get_antoine_coefficient):
    propane_example = get_antoine_coefficient('propane', 350)
    propane_example
    return


@app.cell
def _(fsolve, get_antoine_coefficient, np, plt, raoult_law_kvalue):
    P = 1.01325  # Pressure in bar
    Tguess = 350  # K
    propane = get_antoine_coefficient('propane', Tguess)
    toluene = get_antoine_coefficient('toluene', Tguess)
    antoineCoefs = np.array([propane[0:3], toluene[0:3]])
    T_soln = []
    x_prop = np.linspace(0, 1)
    y_prop = []
    for z_prop in x_prop:
        z = [z_prop, 1 - z_prop]

        def resfun(T):
            return 1 - np.sum(raoult_law_kvalue(T, P, antoineCoefs) * z)
        T = fsolve(resfun, Tguess)
        Tguess = T
        T_soln.append(T)
        K = raoult_law_kvalue(T, P, antoineCoefs)
        y = K * z
        y_prop.append(y[0])
    plt.plot(y_prop, T_soln, label='Y_prop')
    plt.plot(x_prop, T_soln, label='X_prop')
    plt.xlabel('$x_{prop}$, $y_{prop}$')
    plt.ylabel('Temperature (K)')
    plt.title('T-x-y of propane and toluene')
    plt.legend(loc='upper left')
    return


if __name__ == "__main__":
    app.run()
