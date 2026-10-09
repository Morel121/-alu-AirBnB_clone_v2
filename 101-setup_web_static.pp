# Puppet manifest to set up web servers for web_static deployment

exec { 'apt-update':
  command => '/usr/bin/apt-get update',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-update'],
}

file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data'],
}

file { '/data/web_static/releases':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static'],
}

file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  force   => true,
  require => File['/data/web_static/releases/test/index.html'],
}

exec { 'nginx-config-update':
  command => "/bin/sed -i '/server_name _;/a \\    location /hbnb_static {\\n        alias /data/web_static/current/;\\n    }' /etc/nginx/sites-available/default",
  unless  => '/bin/grep -q "location /hbnb_static" /etc/nginx/sites-available/default',
  require => Package['nginx'],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => Exec['nginx-config-update'],
}
