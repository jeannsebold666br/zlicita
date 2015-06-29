<?php
namespace Admin\Form;

use Zend\Form\Form;
use Zend\InputFilter\InputFilter;
use Zend\InputFilter\Factory;

/**
 * Class Login
 * @package Admin\Form
 */
class Login extends Form
{
    /**
     *
     */
    public function __construct()
    {
        parent::__construct('login');
        $this->setAttribute('method', 'post');
        $this->setAttribute('action', '/admin/auth/index');
        
        $this->add(array(
            'name' => 'username',
            'attributes' => array(
                'type'  => 'text',
            ),
            'options' => array(
                'label' => 'Usuário',
                'column-size' => 'sm-4',
                'label_attributes' => array('class' => 'col-sm-2')
            ),
        ));
        $this->add(array(
            'name' => 'password',
            'attributes' => array(
                'type'  => 'password',
            ),
            'options' => array(
                'label' => 'Senha',
                'column-size' => 'sm-4',
                'label_attributes' => array('class' => 'col-sm-2')
            ),
        ));
        $this->add(array(
            'name' => 'submit',
            'attributes' => array(
                'type'  => 'submit',
                'value' => 'Entrar',
                'id' => 'submitbutton',
            ),
            'options' => array(
                'label' => ' ',
                'column-size' => 'sm-4',
                'label_attributes' => array('class' => 'col-sm-2')
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

            $inputFilter->add($factory->createInput(array(
                'name'     => 'username',
                'required' => true,
                'filters'  => array(
                    array('name' => 'StripTags'),
                    array('name' => 'StringTrim'),
                ),
                'validators' => array(
                    array(
                        'name'    => 'StringLength',
                        'options' => array(
                            'encoding' => 'UTF-8',
                            'min'      => 1,
                            'max'      => 50,
                        ),
                    ),
                ),
            )));

            $inputFilter->add($factory->createInput(array(
                'name'     => 'password',
                'required' => true,
                'filters'  => array(
                    array('name' => 'StripTags'),
                    array('name' => 'StringTrim'),
                ),
            )));


        }
        return $inputFilter;
    }

}
