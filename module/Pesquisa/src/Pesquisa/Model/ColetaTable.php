<?php
namespace Pesquisa\Model;

use Zend\Db\TableGateway\AbstractTableGateway;
use Zend\Db\TableGateway\Feature;

/**
 * Class MyTableGateway
 *
 *
 *
 */
class ColetaTable extends AbstractTableGateway
{

    /**
     *
     */
    protected $_primary = 'id_coleta';

    /**
     *
     */
    public function __construct()
    {
        $this->table = 'coleta';
        $this->featureSet = new Feature\FeatureSet();
        $this->featureSet->addFeature(new Feature\GlobalAdapterFeature());
        $this->initialize();
    }
}