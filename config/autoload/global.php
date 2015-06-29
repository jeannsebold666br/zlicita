<?php
/**
 * Global Configuration Override
 *
 * You can use this file for overriding configuration values from modules, etc.
 * You would place values in here that are agnostic to the environment and not
 * sensitive to security.
 *
 * @NOTE: In practice, this file will typically be INCLUDED in your source
 * control, so do not include passwords or other sensitive information in this
 * file.
 */

return array(
    'db' => array(
      'driver'         => 'Pdo',
      'dsn'            => 'mysql:dbname=zlicita;host=localhost',
      'driver_options' => array(
                PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES \'UTF8\''
      ),
   ),
    // Service Manager
    'service_manager' => array(
        'factories' => array(
            'DbAdapter' => function ($serviceManager) {
                $adapterFactory = new Zend\Db\Adapter\AdapterServiceFactory();
                $adapter = $adapterFactory->createService($serviceManager);
                \Zend\Db\TableGateway\Feature\GlobalAdapterFeature::setStaticAdapter($adapter);
                return $adapter;
            }
        ),
    ),

    // Menu Principal
    'navigation' => array(
        'default' => array(
            array(
                'label' => 'Home',
                'route' => 'home',
                'resource' => 'Application\Controller\Index.index',
                'icon' => 'glyphicon glyphicon-home'
            ),
            array(
                'label' => 'Painel',
                'route' => 'admin',
                'resource' => 'Admin\Controller\Index.index',
                'icon' => 'glyphicon glyphicon-th'
            ),
            array(
                'label' => 'Entrar',
                'uri' => '/admin/auth',
                'resource' => 'Admin\Controller\Auth.login',
                'icon' => 'glyphicon glyphicon-log-in'
            ),
            array(
                'label' => 'Sair',
                'uri' => '/admin/auth/logout',
                'resource' => 'Admin\Controller\Auth.logout',
                'icon' => 'glyphicon glyphicon-log-out'
            ),
        ),
    ),

    // Controle de acesso
    'acl' => array(
        'roles' => array(
            'visitante'   => null,
            'admin' => 'visitante'
        ),
        'resources' => array(
            'Application\Controller\Index.index',
            'Admin\Controller\Index.index',
            'Admin\Controller\Auth.index',
            'Admin\Controller\Auth.login',
            'Admin\Controller\Auth.logout',
        ),
        'privilege' => array(
            'visitante' => array(
                'allow' => array(
                    'Application\Controller\Index.index',
                    'Admin\Controller\Auth.index',
                    'Admin\Controller\Auth.login',
                )
            ),
            'admin' => array(
                'allow' => array(
                    'Admin\Controller\Index.index',
                    'Admin\Controller\Auth.logout',
                )
            ),
        )
    ),
);
