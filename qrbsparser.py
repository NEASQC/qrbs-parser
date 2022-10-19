# -*- coding : utf-8 -*-

"""
Test for this module
"""

from neasqc_qrbs import qrbs, knowledge_rep


class QRBSParser():

    def _parse_lefthandside(lhs, system: qrbs.QRBS) -> knowledge_rep.LeftHandSide:
        result = None

        if 'andOperator' in lhs:
            el = lhs['andOperator']
            result = knowledge_rep.AndOperator(
                QRBSParser._parse_lefthandside(el['leftChild'], system),
                QRBSParser._parse_lefthandside(el['rightChild'], system)
            )
        elif 'orOperator' in lhs:
            el = lhs['orOperator']
            result = knowledge_rep.OrOperator(
                QRBSParser._parse_lefthandside(el['leftChild'], system),
                QRBSParser._parse_lefthandside(el['rightChild'], system)
            )
        elif 'notOperator' in lhs:
            el = lhs['notOperator']
            result = knowledge_rep.NotOperator(
                QRBSParser._parse_lefthandside(el['child'], system)
            )
        else:
            fact = lhs['fact']
            result = system.assert_fact(fact['attribute'], fact['value'], fact['imprecission'])
        
        return result

    @staticmethod
    def parse(json, initial_qrbs=None) -> qrbs.QRBS:
        system = qrbs.QRBS() if initial_qrbs is None else initial_qrbs

        if 'islands' in json:
            for island in json['islands']:
                system.assert_island(QRBSParser.parse(island, system))
        elif 'rules' in json:
            for rule in json['rules']:
                system.assert_rule(
                    QRBSParser._parse_lefthandside(rule['leftHandSide'], system),
                    QRBSParser._parse_lefthandside(rule['rightHandSide'], system),
                    rule['uncertainty']
                )

        return system
