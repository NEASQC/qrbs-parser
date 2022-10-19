# -*- coding : utf-8 -*-

"""
Test for this module
"""


from neasqc_qrbs import qrbs, knowledge_rep
from qrbsparser import QRBSParser


class TestQRBSParser:
    """
    Testing QRBSParser
    """

    def test_parse(self):
        test ={
            'islands': [
                {
                    'rules': [
                        {
                            'leftHandSide': {
                                'andOperator': {
                                    'leftChild': {
                                        'fact': {
                                            'attribute': 'test',
                                            'value': 'true',
                                            'imprecission': 0.7
                                        }
                                    },
                                    'rightChild': {
                                        'notOperator': {
                                            'child': {
                                                'fact': {
                                                    'attribute' : 'test2',
                                                    'value': 'false',
                                                    'imprecission': 0.4
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            'rightHandSide': {
                                'fact': {
                                    'attribute': 'result',
                                    'value': 'true',
                                    'imprecission': 0.5
                                }
                            },
                            'uncertainty': 0.1
                        }
                    ]
                }
            ]
        }

        test_result = QRBSParser.parse(test)

        system = qrbs.QRBS()

        fact_test = system.assert_fact('test', 'true', 0.7)
        fact_test2 = system.assert_fact('test2', 'false', 0.4)
        fact_result = system.assert_fact('result', 'true', 0.5)

        rule = system.assert_rule(knowledge_rep.AndOperator(fact_test, knowledge_rep.NotOperator(fact_test2)), fact_result, 0.5)

        island = system.assert_island([rule])

        assert system == test_result
