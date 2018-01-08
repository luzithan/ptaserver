# Create a new Web Droplet running ubuntu in the FRA1 region
resource "digitalocean_droplet" "master" {
    image  = "docker-16-04"
    name   = "terrform-droplet"
    region = "${var.do_region}"
    size   = "1gb"
}

resource "cloudflare_record" "www" {
    domain = "${var.cloudflare_domain}"
    name   = "*"
    type   = "A"
    value  = "${digitalocean_droplet.master.ipv4_address}"
}

resource "docker_image" "nginx" {
  name = "nginx:1.11-alpine"
}

resource "docker_container" "nginx-server" {
  name = "nginx-server"
  image = "${docker_image.nginx.latest}"
  ports {
    internal = 80
  }
  volumes {
    container_path  = "/usr/share/nginx/html"
    host_path = "/home/scrapbook/tutorial/www"
    read_only = true
  }
}
