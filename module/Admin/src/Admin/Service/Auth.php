<?php
namespace Admin\Service;

use Admin\Service\Service;
use Zend\Authentication\AuthenticationService;
use Zend\Authentication\Adapter\DbTable\CredentialTreatmentAdapter as AuthAdapter;
use Zend\Db\Sql\Select;
use Zend\XmlRpc\Request\Stdin;

/**
 * Serviço responsável pela autenticação da aplicação
  *
 * @category Admin
 * @package Service
 * @author  Elton Minetto<eminetto@coderockr.com>
 */
class Auth extends Service
{
    /**
     * Adapter usado para a autenticação
     * @var Zend\Db\Adapter\Adapter
     */
    private $dbAdapter;

    /**
     * @var string
     */
    private $role;

    /**
     * @var string
     */
    private $role_default = "visitante";

    /**
     * Construtor da classe
     *
     * @return void
     */
    public function __construct($dbAdapter = null, $session)
    {
        $this->dbAdapter = $dbAdapter;

        $user = $session->offsetGet('user');
        $role = $this->role_default;
        if(!is_null($user)){
            $role = $user->role;
        }else{
            $user = new \stdClass();
            $user->role = $role;
            $session->offsetSet('user', $user);
        }
        $this->role = $role;
    }


    public function getAcl(){
        return $this->getServiceManager()->get('Admin\Acl\Builder')->build();
    }

    public function getRole(){
        return $this->role;
    }

    /**
     * Faz a autenticação dos usuários
     *
     * @param array $params
     * @return array
     */
    public function authenticate($params)
    {
        if (!isset($params['username']) || !isset($params['password'])) {
            throw new \Exception("Parâmetros inválidos");
        }

        $password = md5($params['password']);
        $auth = new AuthenticationService();
        $authAdapter = new AuthAdapter($this->dbAdapter);
        $authAdapter
            ->setTableName('user')
            ->setIdentityColumn('username')
            ->setCredentialColumn('password')
            ->setIdentity($params['username'])
            ->setCredential($password);
        $result = $auth->authenticate($authAdapter);

        if (! $result->isValid()) {
            throw new \Exception("Login ou senha inválidos");
        }

        //salva o user na sessão
        $session = $this->getServiceManager()->get('Session');
        $session->offsetSet('user', $authAdapter->getResultRowObject());

        return true;
    }


    /**
     * Faz a autorização do usuário para acessar o recurso
     * @param string $moduleName Nome do módulo sendo acessado
     * @param string $controllerName Nome do controller
     * @param string $actionName Nome da ação
     * @return boolean
     */
    public function authorize($moduleName, $controllerName, $actionName)
    {
        $auth = new AuthenticationService();
        $role = 'visitante';
        if ($auth->hasIdentity()) {
            $session = $this->getServiceManager()->get('Session');
            $user = $session->offsetGet('user');
            $role = $user->role;
        }

        $resource = $controllerName . '.' . $actionName;
        $acl = $this->getServiceManager()->get('Admin\Acl\Builder')->build();
        if ($acl->isAllowed($role, $resource)) {
            return true;
        }
        return false;
    }

    /**
     * Faz o logout do sistema
     *
     * @return void
     */
    public function logout() {
        $auth = new AuthenticationService();
        $session = $this->getServiceManager()->get('Session');
        $session->offsetUnset('user');
        $auth->clearIdentity();

        $user = new \stdClass();
        $user->role = $this->role_default;
        $session->offsetSet('user', $user);
        return true;
    }

}