import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go

# Black-Scholes formula for European options
def black_scholes(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return option_price

# Option Greeks
def option_greeks(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
             - r * X * np.exp(-r * T) * norm.cdf(d2)) if option_type == 'call' else (
             -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
             + r * X * np.exp(-r * T) * norm.cdf(-d2))
    rho = X * T * np.exp(-r * T) * norm.cdf(d2) if option_type == 'call' else -X * T * np.exp(-r * T) * norm.cdf(-d2)
    
    return delta, gamma, vega, theta, rho

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Black-Scholes Option Pricing Dashboard with Greeks"),
    
    # Input fields for stock price, strike price, risk-free rate, volatility, and time to maturity
    html.Div([
        html.Label("Stock Price (S)"),
        dcc.Input(id='stock-price', type='number', value=100, step=1),
    ]),
    
    html.Div([
        html.Label("Strike Price (X)"),
        dcc.Input(id='strike-price', type='number', value=100, step=1),
    ]),
    
    html.Div([
        html.Label("Risk-Free Rate (r)"),
        dcc.Input(id='risk-free-rate', type='number', value=0.05, step=0.001),
    ]),
    
    html.Div([
        html.Label("Volatility (σ)"),
        dcc.Input(id='volatility', type='number', value=0.2, step=0.01),
    ]),
    
    html.Div([
        html.Label("Time to Maturity (T) in years"),
        dcc.Slider(id='time-to-maturity', min=0.1, max=3, step=0.1, value=1),
        html.Div(id='time-to-maturity-output')
    ]),

    # Display Call Option Prices and Greeks
    html.Div([
        html.H3("Call Option Prices and Greeks"),
        html.Div(id='call-price-output', style={'font-weight': 'bold'}),
        html.Div(id='call-delta-output', style={'font-weight': 'bold'}),
        html.Div(id='call-gamma-output', style={'font-weight': 'bold'}),
        html.Div(id='call-vega-output', style={'font-weight': 'bold'}),
        html.Div(id='call-theta-output', style={'font-weight': 'bold'}),
        html.Div(id='call-rho-output', style={'font-weight': 'bold'}),
    ]),
    
    # Display Put Option Prices and Greeks
    html.Div([
        html.H3("Put Option Prices and Greeks"),
        html.Div(id='put-price-output', style={'font-weight': 'bold'}),
        html.Div(id='put-delta-output', style={'font-weight': 'bold'}),
        html.Div(id='put-gamma-output', style={'font-weight': 'bold'}),
        html.Div(id='put-vega-output', style={'font-weight': 'bold'}),
        html.Div(id='put-theta-output', style={'font-weight': 'bold'}),
        html.Div(id='put-rho-output', style={'font-weight': 'bold'}),
    ]),

    dcc.Graph(id='pnl-graph'),
])

# Callback to update graph and inputs
@app.callback(
    [
        Output('time-to-maturity-output', 'children'),
        Output('call-price-output', 'children'),
        Output('put-price-output', 'children'),
        Output('call-delta-output', 'children'),
        Output('call-gamma-output', 'children'),
        Output('call-vega-output', 'children'),
        Output('call-theta-output', 'children'),
        Output('call-rho-output', 'children'),
        Output('put-delta-output', 'children'),
        Output('put-gamma-output', 'children'),
        Output('put-vega-output', 'children'),
        Output('put-theta-output', 'children'),
        Output('put-rho-output', 'children'),
        Output('pnl-graph', 'figure')
    ],
    [
        Input('stock-price', 'value'),
        Input('strike-price', 'value'),
        Input('risk-free-rate', 'value'),
        Input('volatility', 'value'),
        Input('time-to-maturity', 'value')
    ]
)
def update_graph(S, X, r, sigma, T):
    # Handle invalid inputs (e.g., None values, negative inputs)
    if S is None or X is None or r is None or sigma is None or T is None or S <= 0 or X <= 0 or r < 0 or sigma <= 0:
        return (
            "Invalid input", "Invalid input", "Invalid input", 
            "Invalid Delta", "Invalid Gamma", "Invalid Vega", "Invalid Theta", "Invalid Rho",
            "Invalid Delta", "Invalid Gamma", "Invalid Vega", "Invalid Theta", "Invalid Rho", go.Figure()
        )

    # Compute the option prices using Black-Scholes
    call_price = black_scholes(S, X, T, r, sigma, 'call')
    put_price = black_scholes(S, X, T, r, sigma, 'put')

    # Compute the Greeks for call and put options
    call_delta, call_gamma, call_vega, call_theta, call_rho = option_greeks(S, X, T, r, sigma, 'call')
    put_delta, put_gamma, put_vega, put_theta, put_rho = option_greeks(S, X, T, r, sigma, 'put')
    
    # Create stock price range for PnL calculation
    stock_prices = np.linspace(0.5 * S, 1.5 * S, 100)
    call_pnl = np.maximum(stock_prices - X, 0) - call_price
    put_pnl = np.maximum(X - stock_prices, 0) - put_price

    # Create figure
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=stock_prices, y=call_pnl, mode='lines', name='Call PnL'))
    figure.add_trace(go.Scatter(x=stock_prices, y=put_pnl, mode='lines', name='Put PnL'))

    figure.update_layout(
        title="PnL of Call and Put Options",
        xaxis_title="Stock Price at Expiration",
        yaxis_title="PnL",
        legend_title="Option Type"
    )

    # Format outputs for call and put options
    call_price_output = f"Call Option Price: ${call_price:.2f}"
    put_price_output = f"Put Option Price: ${put_price:.2f}"
    
    call_delta_output = f"Delta: {call_delta:.4f}"
    call_gamma_output = f"Gamma: {call_gamma:.4f}"
    call_vega_output = f"Vega: {call_vega:.4f}"
    call_theta_output = f"Theta: {call_theta:.4f}"
    call_rho_output = f"Rho: {call_rho:.4f}"
    
    put_delta_output = f"Delta: {put_delta:.4f}"
    put_gamma_output = f"Gamma: {put_gamma:.4f}"
    put_vega_output = f"Vega: {put_vega:.4f}"
    put_theta_output = f"Theta: {put_theta:.4f}"
    put_rho_output = f"Rho: {put_rho:.4f}"

    return (
        f"Time to Maturity: {T:.2f} years",
        call_price_output,
        put_price_output,
        call_delta_output,
        call_gamma_output,
        call_vega_output,
        call_theta_output,
        call_rho_output,
        put_delta_output,
        put_gamma_output,
        put_vega_output,
        put_theta_output,
        put_rho_output,
        figure
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
