from flask_assets import Bundle

bundles = {

    'home_js': Bundle(
        'js/vendor/jquery-3.3.1.js',
        'js/vendor/popper.js',
        'js/vendor/bootstrap.js',
        filters='jsmin',
        output='gen/home.js'),

    'home_css': Bundle(
        'css/vendor/bootstrap4.css',
        'css/user.css',
        filters='cssmin',
        output='gen/home.css'),

    # 'admin_js': Bundle(
    #     'js/lib/jquery-1.10.2.js',
    #     'js/lib/Chart.js',
    #     'js/admin.js',
    #     output='gen/admin.js'),

    # 'admin_css': Bundle(
    #     'css/lib/reset.css',
    #     'css/common.css',
    #     'css/admin.css',
    #     output='gen/admin.css')
}


