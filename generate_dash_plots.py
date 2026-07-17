import pandas as pd
import plotly.express as px
import plotly.io as pio

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Slide 39: Launch success count for all sites, in a piechart
pie_data = df.groupby('LaunchSite')['Class'].sum().reset_index()
fig1 = px.pie(pie_data, values='Class', names='LaunchSite', title='Total Success Launches by Site')
fig1.write_image("plots/dash_all_sites_pie.png")

# Slide 40: Piechart for the launch site with the highest launch success ratio
site_data = df[df['LaunchSite'] == 'KSC LC 39A']
site_pie_data = site_data['Class'].value_counts().reset_index()
site_pie_data.columns = ['Class', 'count']
fig2 = px.pie(site_pie_data, values='count', names='Class', title='Total Success Launches for site KSC LC 39A')
fig2.write_image("plots/dash_best_site_pie.png")

# Slide 41: Payload vs. Launch Outcome scatter plot for all sites
fig3 = px.scatter(df, x='PayloadMass', y='Class', color='BoosterVersion', title='Correlation between Payload and Success for all Sites')
fig3.write_image("plots/dash_payload_scatter.png")

print("Dash plots generated.")
