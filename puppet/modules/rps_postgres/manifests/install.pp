class rps_postgres::install {
    class {'postgresql::server': }

    # FIXME: This is to simplify the configuration for development
    postgresql::server::pg_hba_rule {'allow unix socket connections to access anything':
        type        => 'local',
        database    => 'all',
        user        => 'all',
        auth_method => 'trust',
    }

    postgresql::server::role { 'ubuntu': }
}
