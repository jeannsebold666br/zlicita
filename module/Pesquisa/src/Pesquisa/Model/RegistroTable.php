<?php
namespace Pesquisa\Model;

use Zend\Db\Sql\Predicate\Predicate;
use Zend\Db\TableGateway\AbstractTableGateway;
use Zend\Db\TableGateway\Feature;
use Zend\Paginator\Adapter\DbSelect;
use Zend\Paginator\Paginator;
use Zend\Db\Sql\Sql;


/**
 * Class MyTableGateway
 *
 *
 *
 */
class RegistroTable extends AbstractTableGateway
{

    /**
     *
     */
    protected $_primary = 'id_registro';

    /**
     *
     */
    public function __construct()
    {
        $this->table = 'registro';
        $this->featureSet = new Feature\FeatureSet();
        $this->featureSet->addFeature(new Feature\GlobalAdapterFeature());
        $this->initialize();
    }


    /**
     * @param $data
     * @return Paginator
     *
     */
    public function pesquisar($data){
        $sql = new Sql($this->getAdapter());
        $select = $this->getSql()->select();
        $select->join('coleta','coleta.id_coleta = registro.id_coleta',array('data'));


        $validator = new \Zend\Validator\Date();

        if($validator->isValid($data["data_ini"]) AND !$validator->isValid($data["data_end"])){
            $select->where->greaterThanOrEqualTo('coleta.data',$data["data_ini"]);
        }

        if(!$validator->isValid($data["data_ini"]) AND $validator->isValid($data["data_end"])){
            $select->where->lessThanOrEqualTo('coleta.data',$data["data_end"]);
        }

        if($validator->isValid($data["data_ini"]) AND $validator->isValid($data["data_end"])){
            $select->where->greaterThanOrEqualTo('coleta.data',$data["data_ini"]);
            $select->where->and->lessThanOrEqualTo('coleta.data', $data["data_end"]);
        }



        if(strlen($data["palavra"]) > 2){
            if($validator->isValid($data["data_ini"]) OR $validator->isValid($data["data_end"])) {
                $select->where->and;
            }

            $select->where->like('registro.cidade','%'.$data["palavra"].'%');
            $select->where->or->like('registro.estado','%'.$data["palavra"].'%');
            $select->where->or->like('registro.objeto','%'.$data["palavra"].'%');
            $select->where->or->like('registro.uasg','%'.$data["palavra"].'%');
            $select->where->or->like('registro.orgao1','%'.$data["palavra"].'%');
            $select->where->or->like('registro.orgao2','%'.$data["palavra"].'%');
            $select->where->or->like('registro.orgao3','%'.$data["palavra"].'%');
            $select->where->or->like('registro.edital','%'.$data["palavra"].'%');
            $select->where->or->like('registro.item_material','%'.$data["palavra"].'%');
            $select->where->or->like('registro.item_servico','%'.$data["palavra"].'%');

        }

        $select->order("coleta.data");

        //echo $select->getSqlString();

        $adapter = new DbSelect($select, $sql);
        $paginator = new Paginator($adapter);
        return $paginator;
    }


    public function find($id)
    {
        if(!($id > 0)){
            return array();
        }

        $rowset = $this->select(array('id_registro' => $id));
        $row = $rowset->current();

        if (!$row) {
            throw new \Exception("Registro não encontrado para #$id");
        }

        return $row;
    }
}