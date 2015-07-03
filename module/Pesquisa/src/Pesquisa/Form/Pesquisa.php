<?php
namespace Pesquisa\Form;

use Zend\Form\Form;
use Zend\InputFilter\InputFilter;
use Zend\InputFilter\Factory;

/**
 * Class Login
 * @package Admin\Form
 */
class Pesquisa extends Form
{
    /**
     *
     */
    public function __construct()
    {
        parent::__construct('pesquisa');
        $this->setAttribute('name', 'pesquisa');
        $this->setAttribute('method', 'post');
        $this->setAttribute('action', '/pesquisa/index/index');
        
        $this->add(array(
            'name' => 'data_ini',
            'attributes' => array(
                'type'  => 'date',
                'placeholder' => 'Data início',
            ),
        ))->add(array(
            'name' => 'data_end',
            'attributes' => array(
                'type'  => 'date',
                'placeholder' => 'Data fim',
            ),
        ))->add(array(
            'name' => 'palavra',
            'attributes' => array(
                'type'  => 'text',
                'placeholder' => 'Palavra chave',
            ),
            'options' => array(
                'column-size' => 'sm-6',
            )
        ))->add(array(
            'name' => 'submit',
            'attributes' => array(
                'type'  => 'submit',
                'id' => 'submitbutton',
            ),
            'options' => array(
                'label' => '',
                'glyphicon' => 'search'
            ),
        ))->add(array(
            'name' => 'clear',
            'attributes' => array(
                'type'  => 'submit',
                'id' => 'clearbutton',
            ),
            'options' => array(
                'label' => '',
                'glyphicon' => 'remove'
            ),
        ));


        $this->setInputFilter($this->getFilter());
    }


    /**
     * Configura os filtros dos campos
     *
     * @return Zend\InputFilter\InputFilter
    */
    public function getFilter()
    {
        if (!$this->inputFilter) {
            $inputFilter = new InputFilter();
            $factory = new Factory();


        }
        return $inputFilter;
    }

}
