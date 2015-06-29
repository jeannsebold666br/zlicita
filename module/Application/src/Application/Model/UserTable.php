<?php
namespace Admin\Model;

use Zend\Db\TableGateway\AbstractTableGateway;
use Zend\Db\TableGateway\Feature;

/**
 * Class MyTableGateway
 *
 *
 *
 */
class UserTable extends AbstractTableGateway
{

    /**
     *
     */
    protected $_primary = 'id_user';

    /**
     *
     */
    public function __construct()
    {
        $this->table = 'user';
        $this->featureSet = new Feature\FeatureSet();
        $this->featureSet->addFeature(new Feature\GlobalAdapterFeature());
        $this->initialize();
    }
}
