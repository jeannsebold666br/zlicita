<?php
/**
 * Zend Framework (http://framework.zend.com/)
 *
 * @link      http://github.com/zendframework/ZendSkeletonApplication for the canonical source repository
 * @copyright Copyright (c) 2005-2015 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace Application;

use Zend\Mvc\ModuleRouteListener;
use Zend\Mvc\MvcEvent;

class Module
{
    public function onBootstrap(MvcEvent $e)
    {
        $eventManager        = $e->getApplication()->getEventManager();
        $moduleRouteListener = new ModuleRouteListener();
        $moduleRouteListener->attach($eventManager);

        /* Translator */
        $translator = $e->getApplication()->getServiceManager()->get('translator');
        $translator->addTranslationFile(
            'phpArray',
            './vendor/zendframework/zend-i18n-resources/languages/pt_BR/Zend_Validate.php',
            'default', 'pt_BR'
        );
        \Zend\Validator\AbstractValidator::setDefaultTranslator($translator);


        /* Injeta o ACL e o usuário no Navigator */
        $auth = $e->getApplication()->getServiceManager()->get('Admin\Service\Auth');
        $acl = $auth->getAcl();
        $role = $auth->getRole();
        \Zend\View\Helper\Navigation::setDefaultAcl($acl);
        \Zend\View\Helper\Navigation::setDefaultRole($role);

        // Remove itens do menu
        if ($role == 'admin') {
            $container = $e->getApplication()->getServiceManager()->get('navigation');
            $home = $container->findBy('route' , 'home');
            $entrar = $container->findBy('uri' , '/admin/auth');
            $container->removePage($home);
            $container->removePage($entrar);
        }

    }

    public function getConfig()
    {
        return include __DIR__ . '/config/module.config.php';
    }

    public function getAutoloaderConfig()
    {
        return array(
            'Zend\Loader\StandardAutoloader' => array(
                'namespaces' => array(
                    __NAMESPACE__ => __DIR__ . '/src/' . __NAMESPACE__,
                ),
            ),
        );
    }
}
