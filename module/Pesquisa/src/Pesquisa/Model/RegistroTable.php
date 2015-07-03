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


    /**
     *
     * @param $id
     * @return array|\ArrayObject|null
     * @throws \Exception
     */
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


    /**
     * @return array
     *
     */
    public function relatorioGeral(){
        $adapter = $this->getAdapter();
        $sql = "SELECT COUNT(*) AS 'total_dias' FROM coleta";
        $statement = $adapter->query($sql);
        $results = $statement->execute();
        $row = $results->current();
        $total_dias = $row['total_dias'];


        $sql = "SELECT
                    (SELECT MIN(data) AS 'min_dia' FROM coleta) AS 'min_dia',
                    (SELECT MAX(data) AS 'max_dia' FROM coleta) AS 'max_dia'";
        $statement = $adapter->query($sql);
        $results = $statement->execute();
        $row = $results->current();
        $min_dia = $row['min_dia'];
        $max_dia = $row['max_dia'];


        $adapter = $this->getAdapter();
        $sql = "SELECT COUNT(*) AS 'total_registros' FROM registro";
        $statement = $adapter->query($sql);
        $results = $statement->execute();
        $row = $results->current();
        $total_registros = $row['total_registros'];


        $adapter = $this->getAdapter();
        $sql = "SELECT COUNT(*) AS 'total_cidades' FROM (SELECT DISTINCT(cidade) FROM registro) AS a";
        $statement = $adapter->query($sql);
        $results = $statement->execute();
        $row = $results->current();
        $total_cidades = $row['total_cidades'];


        $adapter = $this->getAdapter();
        $sql = "SELECT table_schema AS 'Database name', SUM(data_length + index_length) / 1024 / 1024 AS 'tamanho_schema'
                FROM information_schema.TABLES
                WHERE  table_schema = '".$this->getAdapter()->getDriver()->getConnection()->getCurrentSchema()."'
                GROUP BY table_schema;";
        $statement = $adapter->query($sql);
        $results = $statement->execute();
        $row = $results->current();
        $tamanho_schema = (int)$row['tamanho_schema'];


        return array(
            'total_dias'        => $total_dias,
            'min_dia'           => $min_dia,
            'max_dia'           => $max_dia,
            'total_registros'   => $total_registros,
            'total_cidades'     => $total_cidades,
            'total_cidades'     => $total_cidades,
            'tamanho_schema'    => $tamanho_schema,
        );

    }
}