<?php
/**
 * Zend Framework (http://framework.zend.com/)
 *
 * @link      http://github.com/zendframework/ZendSkeletonApplication for the canonical source repository
 * @copyright Copyright (c) 2005-2015 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace Admin\Controller;

use Zend\Mvc\Controller\AbstractActionController;
use Zend\View\Model\ViewModel;
use Admin\Form\Login;

/**
 * Class AuthController
 * @package Admin\Controller
 *
 * Controla a autenticação do usuário
 */
class AuthController extends AbstractActionController
{
    /**
     * Faz login do usuário
     *
     * @return \Zend\Http\Response|ViewModel
     */
    public function indexAction()
    {
        $form = new Login();
        $request = $this->getRequest();

        if ($request->isPost()) {
            $form->setData($request->getPost());

            if ($form->isValid()) {
                $data = $form->getData();

                $service = $this->getServiceLocator()->get('Admin\Service\Auth');
                try {
                    $auth = $service->authenticate(
                        array('username' => $data['username'], 'password' => $data['password'])
                    );
                    return $this->redirect()->toUrl('/admin');

                }catch (\Exception $e) {
                    $message = "";
                    if ($e->getCode() == 0){
                        $message = $e->getMessage();
                    }else{
                        $message = "Erro do sistema. Favor contactar o administrador.";
                    }
                    $this->flashMessenger()->addErrorMessage($message);
                }
            }
        }


        return new ViewModel(array(
            'form' => $form,
        ));
    }

    /**
     * Faz o logout do usuário
     * @return void
    */
    public function logoutAction()
    {
        $service =  $this->getServiceLocator()->get('Admin\Service\Auth');
        $auth = $service->logout();

        return $this->redirect()->toUrl('/');
    }


}
