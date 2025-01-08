<!-- ---------------------------------------------------------------------- -->
<h1>Notarial Support in Neo4j</h1>
<!-- ---------------------------------------------------------------------- -->
<dir>
    <hr>
    <p>
        Notarial support project in Python & Neo4j.<br/>
        Connect to a Neo4j database and execute a series of operations to control
        the status of the inheritance of the family's goods.<br/>
    </p>
    <hr>
    <h2>Dataset</h2>
    <i>Neo_DB.txt</i> --> Dataset used for the notarial support. The dataset is 
                          created by the work team.<br/><br/>
    
    
    <h3>Element description</h3>
    <table>
        <caption>The dataset is composed of five types of data</caption>
        <tr>
           <td>p                 </td>
           <td>Person            </td>
        </tr>
        <tr><td>bi               </td>
            <td>Immovable goods  </td>
        </tr>
        <tr>
           <td>bm                </td>
           <td>Movable goods     </td>
        </tr>
        <tr>
           <td>cc                </td>
           <td>Bank Account      </td>
        </tr>
        <tr>
           <td>s                 </td>
           <td>Country           </td>
        </tr>
    </table>
    
    <br/>
</dir>
-------------------------------------------------------------------------------
<h4>Person (p)</h4>
-------------------------------------------------------------------------------
<dir>
    <br/>
    
    An example of a person is:<br/>
    
    <pre><i>CREATE(ROSIL01ISOLD09OL:p {name: "Astolfo",
           surname: "Rossi",   
           id: "ROSIL01ISOLD09OL",   
           status: "alive",
           age: 90 })</i></pre><br/>
    
    <p>
       Where <i>ROSIL01ISOLD09OL</i> is the unique key that identifies the person, and it is the same
       as the ID.
    </p>
    <br/>
    
    <table>
        <caption>Person Attributes</caption>
        <tr>
            <td>name                              </td>
            <td>Name of the person                </td>
        </tr>
        <tr>
            <td>surname                           </td>
            <td>Surname of the person             </td>
        </tr>
        <tr>
            <td>id                                </td>
            <td>Identification code of the person </td>
        </tr>
        <tr>
            <td>status                            </td>
            <td>Alive or deceased                 </td>
        </tr>
        <tr>
            <td>age                               </td>
            <td>Age                               </td>
        </tr>
    </table>
       
    <br/>
</dir>
-------------------------------------------------------------------------------
<h4>Immovable Good (bi)</h4>
-------------------------------------------------------------------------------
<dir>
    <br/>
    
    <pre><i>CREATE(bi0:b {name: "House in the Alps",
                    value: 500000,
    				code: 'bi0'})</i></pre><br/>
    
    <p>
        Where <i>bi0</i> is the unique identification of the immovable good.
    </p>
    <br/>
    
    <table>
        <caption>Immovable Good Attributes</caption>
        <tr>
            <td>name                                   </td>
            <td>Name of the goods                      </td>
        </tr>
        <tr>
            <td>value                                  </td>
            <td>Value in euros                         </td>
        </tr>
        <tr>
            <td>code                                   </td>
            <td>Same code as the unique identification </td>
        </tr>
    </table>
    
    <br/>
</dir>
-------------------------------------------------------------------------------
<h4>Movable Good (bm)</h4>
-------------------------------------------------------------------------------
<dir>
    <br/>
    
    <pre>
        <i>CREATE(bm0:b {name: "Alfa Giulia",
                    value: 40000,
    				code: 'bm0'})
    	</i>
    </pre>
    <br/>
    
    
    <p>
        Where <i>bm0</i> is the unique identification of the movable good.
    </p>
    <br/>
    
    <table>
        <caption>Movable Good Attributes</caption>
        <tr>
            <td>name              </td>
            <td>Name of the goods </td>
        </tr>
        <tr>
            <td>value             </td>
            <td>Value in euros    </td>
        </tr>
        <tr>
            <td>code                                   </td>
            <td>Same code as the unique identification </td>
        </tr>
    </table>
    
    <br/>
</dir>
-------------------------------------------------------------------------------
<h4>Bank Account (cc)</h4>
-------------------------------------------------------------------------------
<dir>
    <br/>
    
    
    <pre>
        <i>
            CREATE(cc0:b {name: "Bank Account Intesa",
                    value: 4000,
    				code: 'cc0'})
    	</i>
    </pre>
    <br/>
    
    <p>
        Where <i>cc0</i> is the unique identification of the bank account.
    </p>
    <br/>
    
    <table>
        <caption>Bank Account Attributes</caption>
        <tr>
            <td>name                 </td>
            <td>Name of the bank account </td>
        </tr>
        <tr>
            <td>value                     </td>
            <td>Money in the bank account </td>
        </tr>
        <tr>
            <td>code                                   </td>
            <td>Same code as the unique identification </td>
        </tr>
    </table>
    
    <br/>
</dir>
-------------------------------------------------------------------------------
<h4>Country (s)</h4>
-------------------------------------------------------------------------------
<dir>
    <br/>
    
    <p>
         There is one country. If a person dies and does not have any parents, siblings, or
         children, the goods of the person become the property of the country.
    </p>
    <br/>
    
    <pre>
        <i>
            CREATE(s:country {name: "Italy"})
        </i>
    </pre>
    <br/>
</dir>
<!-- ---------------------------------------------------------------------- -->
