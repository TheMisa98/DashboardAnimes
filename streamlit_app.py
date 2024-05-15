import plotly.express as px
import pandas as pd
import streamlit as st
from queries_olap import Queries

qr = Queries()
top_10_anime = qr.get_top_10_anime() 
print(top_10_anime)