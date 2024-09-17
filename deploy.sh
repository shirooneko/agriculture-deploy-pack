# deploy.sh

# Menyalin semua file dari direktori saat ini ke dalam container
sudo docker cp . odoo17-container:/usr/lib/python3/dist-packages/odoo/addons/

# Restart container Odoo
sudo docker restart odoo17-container
