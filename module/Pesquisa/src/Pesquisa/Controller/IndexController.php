<?php
/**
 * Zend Framework (http://framework.zend.com/)
 *
 * @link      http://github.com/zendframework/ZendSkeletonApplication for the canonical source repository
 * @copyright Copyright (c) 2005-2015 Zend Technologies USA Inc. (http://www.zend.com)
 * @license   http://framework.zend.com/license/new-bsd New BSD License
 */

namespace Pesquisa\Controller;

use Zend\Mvc\Controller\AbstractActionController;
use Zend\View\Model\ViewModel;
use Pesquisa\Form\Pesquisa;
use Pesquisa\Model\RegistroTable;

class IndexController extends AbstractActionController
{
    public function indexAction()
    {
        $form = new Pesquisa();
        $request = $this->getRequest();
        $page = $this->params()->fromRoute('page',1);
        $paginator = array();
        $session =  $this->getServiceLocator()->get('Session');
        $reset = false;

        $user = $session->offsetGet('user');


        if ($request->isPost()) {
            $message = "";
            $post = $request->getPost();

            if(is_null($post['clear'])) {

                $form->setData($post);

                if ($form->isValid()) {
                    $data = $form->getData();
                    $user->pesquisa = $data;
                }
            }else{
                unset($user->pesquisa);
                $form->setData(array());
                $data = array();
                $reset = true;
            }

            $session->offsetSet('user', $user);

        }

        //var_dump($data);
        //var_dump($user->pesquisa);

        if(isset($user->pesquisa)) {
            $registro = new RegistroTable();
            $data = $user->pesquisa;
            $form->setData($data);
            $id = $this->params()->fromRoute('');

            try {
                $paginator = $registro->pesquisar($data);
                $paginator->setCurrentPageNumber($page)
                    ->setItemCountPerPage(100)
                    ->setPageRange(20);

                if (count($paginator) == 0) {
                    $message = "Nenhum registro encontrado.";
                }

            } catch (\Exception $e) {

                //if ($e->getCode() == 0){
                    $message = $e->getMessage();
                //}else{
                //$message = "Erro do sistema. Favor contactar o administrador.";
                //}

                if (strlen($message) > 0) {
                    $this->flashMessenger()->addErrorMessage($message);
                }
            }
        }

        return new ViewModel(array(
            'form' => $form,
            'paginator' => $paginator,
            'reset' => $reset,
        ));
    }


    public function registroAction()
    {
        $id = $this->params()->fromRoute('id');
        $registro = new RegistroTable();
        $result = $registro->find($id);


        return new ViewModel(array(
            'registro' => $result,
        ));
    }
}
