# Black-Scholes Option Pricing Dashboard with Greeks
This project implements a web-based dashboard that calculates and visualizes option prices and Greeks for European Call and Put options using the Black-Scholes model. The dashboard is built with Dash (a Python web framework) and allows users to interactively input parameters like stock price, strike price, volatility, risk-free rate, and time to maturity.

**Features**
Black-Scholes Option Pricing:

Calculates the price of European Call and Put options using the Black-Scholes formula.
Option Greeks:

Displays the Greeks (Delta, Gamma, Vega, Theta, and Rho) for both Call and Put options:
Delta: Sensitivity of the option price to the underlying asset's price.
Gamma: Rate of change of Delta with respect to changes in the underlying asset's price.
Vega: Sensitivity to changes in volatility.
Theta: Sensitivity to the passage of time (time decay).
Rho: Sensitivity to changes in the risk-free interest rate.
PnL Visualization:

Plots the Profit and Loss (PnL) for both Call and Put options based on a range of possible underlying stock prices.
Interactive Inputs:

**Users can interactively input values for:**
Stock price (S)
Strike price (X)
Risk-free rate (r)
Volatility (σ)
Time to maturity (T)
The dashboard updates the option prices, Greeks, and PnL visualization in real-time.
