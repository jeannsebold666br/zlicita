<?php
/**
 * Zend Framework (http://framework.zend.com/)
 *
 * @link      http://github.com/zendframework/ZendSkeletonApplication for the canonical source repository
 * @copyright Copyright (c) 2005-2015 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

return array(
    'controllers' => array(
        'invokables' => array(
            'Pesquisa\Controller\Index' => 'Pesquisa\Controller\IndexController'
        ),
    ),

    'router' => array(
        'routes' => array(
            // The following is a route to simplify getting started creating
            // new controllers and actions without needing to create a new
            // module. Simply drop new controllers in, and you can access them
            // using the path /application/:controller/:action
            'pesquisa' => array(
                'type'    => 'Literal',
                'options' => array(
                    'route'    => '/pesquisa',
                    'defaults' => array(
                        '__NAMESPACE__' => 'Pesquisa\Controller',
                        'controller'    => 'Index',
                        'action'        => 'index',
                        'module'        => 'admin'
                    ),
                ),
                'may_terminate' => true,
                'child_routes' => array(
                    'default' => array(
                        'type'    => 'segment',
                        'options' => array(
                            'route'    => '/[:controller[/:action]][/page/:page][/id/:id]',
                            'constraints' => array(
                                'controller' => '[a-zA-Z][a-zA-Z0-9_-]*',
                                'action'     => '[a-zA-Z][a-zA-Z0-9_-]*',
                                'page'       => '[0-9]+',
                                'id'       => '[0-9]+',
                            ),
                            'defaults' => array(
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),

    // Menu Principal
    'navigation' => array(
        'default' => array(
            array(
                'label' => 'Pesquisa',
                'route' => 'pesquisa',
                'resource' => 'Pesquisa\Controller\Index.index',
                'icon' => 'glyphicon glyphicon-search',
                'order' => 1,
            ),

        ),
    ),


    // Controle de acesso
    'acl' => array(
        'resources' => array(
            'Pesquisa\Controller\Index.index',
            'Pesquisa\Controller\Index.registro',
        ),
        'privilege' => array(
            'admin' => array(
                'allow' => array(
                    'Pesquisa\Controller\Index.index',
                    'Pesquisa\Controller\Index.registro',
                )
            ),
        )
    ),



    'view_manager' => array(
        'template_path_stack' => array(
            'album' => __DIR__ . '/../view',
        ),
    ),

);
